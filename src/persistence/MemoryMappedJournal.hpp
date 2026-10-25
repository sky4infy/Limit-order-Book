#pragma once

#include "../common/Types.hpp"
#include <cstdint>
#include <string>
#include <vector>
#include <stdexcept>
#include <cstring>
#include <iostream>

#if defined(_WIN32)
#ifndef NOMINMAX
#define NOMINMAX
#endif
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#else
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#endif

namespace lob {

enum class JournalEventType : uint8_t {
    ORDER_ADD = 1,
    ORDER_CANCEL = 2,
    ORDER_EXECUTE = 3
};

#pragma pack(push, 1)
struct JournalHeader {
    char magic[8];         // "LOBJRNL"
    uint64_t version;      // 1
    uint64_t write_offset; // Absolute byte offset for next write
    uint64_t record_count; // Total records committed
    uint64_t last_seq;     // Last sequence number
    uint8_t reserved[24];
};

struct JournalRecord {
    uint64_t sequence_number;
    uint64_t timestamp;
    uint8_t event_type;
    uint64_t order_id;
    uint32_t firm_id;
    uint8_t side;
    Price price;
    Quantity quantity;
    uint32_t checksum;
};
#pragma pack(pop)

static_assert(sizeof(JournalHeader) == 64, "JournalHeader must be exactly 64 bytes packed");
static_assert(sizeof(JournalRecord) == 46, "JournalRecord must be exactly 46 bytes packed");

class MemoryMappedJournal {
public:
    explicit MemoryMappedJournal(const std::string& filepath, size_t file_size = 64 * 1024 * 1024)
        : filepath_(filepath), max_size_(file_size), write_offset_(sizeof(JournalHeader)), sequence_counter_(0)
    {
        init_mapping();
    }

    ~MemoryMappedJournal() {
        close_mapping();
    }

    // Append record with zero dynamic allocation
    inline bool append(JournalEventType event_type, uint64_t timestamp, uint64_t order_id,
                       uint32_t firm_id, Side side, Price price, Quantity qty) noexcept 
    {
        if (write_offset_ + sizeof(JournalRecord) > max_size_) [[unlikely]] {
            return false; // Journal file capacity reached
        }

        uint64_t seq = ++sequence_counter_;
        
        // Fast XOR checksum for integrity
        uint32_t csum = static_cast<uint32_t>(seq ^ timestamp ^ order_id ^ price ^ qty);

        JournalRecord* rec = reinterpret_cast<JournalRecord*>(base_ptr_ + write_offset_);
        rec->sequence_number = seq;
        rec->timestamp = timestamp;
        rec->event_type = static_cast<uint8_t>(event_type);
        rec->order_id = order_id;
        rec->firm_id = firm_id;
        rec->side = static_cast<uint8_t>(side);
        rec->price = price;
        rec->quantity = qty;
        rec->checksum = csum;

        write_offset_ += sizeof(JournalRecord);

        // Update header in-place
        JournalHeader* hdr = reinterpret_cast<JournalHeader*>(base_ptr_);
        hdr->write_offset = write_offset_;
        hdr->record_count++;
        hdr->last_seq = seq;

        return true;
    }

    // Direct memory pointer sequential replay
    std::vector<JournalRecord> replay_all() const {
        std::vector<JournalRecord> records;
        const JournalHeader* hdr = reinterpret_cast<const JournalHeader*>(base_ptr_);
        if (std::memcmp(hdr->magic, "LOBJRNL", 7) != 0) {
            return records;
        }

        size_t count = static_cast<size_t>(hdr->record_count);
        records.reserve(count);

        const JournalRecord* recs = reinterpret_cast<const JournalRecord*>(base_ptr_ + sizeof(JournalHeader));
        for (size_t i = 0; i < count; ++i) {
            records.push_back(recs[i]);
        }
        return records;
    }

    size_t record_count() const noexcept {
        const JournalHeader* hdr = reinterpret_cast<const JournalHeader*>(base_ptr_);
        return hdr ? static_cast<size_t>(hdr->record_count) : 0;
    }

    size_t bytes_written() const noexcept {
        return write_offset_;
    }

    void sync() {
#if defined(_WIN32)
        if (base_ptr_) FlushViewOfFile(base_ptr_, write_offset_);
#else
        if (base_ptr_) msync(base_ptr_, write_offset_, MS_SYNC);
#endif
    }

private:
    void init_mapping() {
#if defined(_WIN32)
        file_handle_ = CreateFileA(
            filepath_.c_str(),
            GENERIC_READ | GENERIC_WRITE,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            NULL,
            OPEN_ALWAYS,
            FILE_ATTRIBUTE_NORMAL,
            NULL
        );
        if (file_handle_ == INVALID_HANDLE_VALUE) {
            throw std::runtime_error("Failed to open journal file: " + filepath_);
        }

        bool existed = (GetLastError() == ERROR_ALREADY_EXISTS);

        mapping_handle_ = CreateFileMappingA(
            file_handle_,
            NULL,
            PAGE_READWRITE,
            static_cast<DWORD>((max_size_ >> 32) & 0xFFFFFFFF),
            static_cast<DWORD>(max_size_ & 0xFFFFFFFF),
            NULL
        );
        if (!mapping_handle_) {
            CloseHandle(file_handle_);
            throw std::runtime_error("Failed to create file mapping for journal");
        }

        base_ptr_ = static_cast<char*>(MapViewOfFile(mapping_handle_, FILE_MAP_ALL_ACCESS, 0, 0, max_size_));
        if (!base_ptr_) {
            CloseHandle(mapping_handle_);
            CloseHandle(file_handle_);
            throw std::runtime_error("Failed to map view of file for journal");
        }

        JournalHeader* hdr = reinterpret_cast<JournalHeader*>(base_ptr_);
        if (existed && std::memcmp(hdr->magic, "LOBJRNL", 7) == 0) {
            write_offset_ = static_cast<size_t>(hdr->write_offset);
            sequence_counter_ = hdr->last_seq;
        } else {
            std::memset(hdr, 0, sizeof(JournalHeader));
            std::memcpy(hdr->magic, "LOBJRNL", 7);
            hdr->version = 1;
            hdr->write_offset = sizeof(JournalHeader);
            hdr->record_count = 0;
            hdr->last_seq = 0;
            write_offset_ = sizeof(JournalHeader);
            sequence_counter_ = 0;
        }
#else
        fd_ = open(filepath_.c_str(), O_RDWR | O_CREAT, 0666);
        if (fd_ < 0) throw std::runtime_error("Failed to open journal file");
        struct stat st;
        fstat(fd_, &st);
        bool existed = (st.st_size >= static_cast<off_t>(sizeof(JournalHeader)));
        if (ftruncate(fd_, max_size_) != 0) throw std::runtime_error("ftruncate failed");
        base_ptr_ = static_cast<char*>(mmap(nullptr, max_size_, PROT_READ | PROT_WRITE, MAP_SHARED, fd_, 0));
        if (base_ptr_ == MAP_FAILED) throw std::runtime_error("mmap failed");

        JournalHeader* hdr = reinterpret_cast<JournalHeader*>(base_ptr_);
        if (existed && std::memcmp(hdr->magic, "LOBJRNL", 7) == 0) {
            write_offset_ = static_cast<size_t>(hdr->write_offset);
            sequence_counter_ = hdr->last_seq;
        } else {
            std::memset(hdr, 0, sizeof(JournalHeader));
            std::memcpy(hdr->magic, "LOBJRNL", 7);
            hdr->version = 1;
            hdr->write_offset = sizeof(JournalHeader);
            hdr->record_count = 0;
            hdr->last_seq = 0;
            write_offset_ = sizeof(JournalHeader);
            sequence_counter_ = 0;
        }
#endif
    }

    void close_mapping() {
        sync();
#if defined(_WIN32)
        if (base_ptr_) UnmapViewOfFile(base_ptr_);
        if (mapping_handle_) CloseHandle(mapping_handle_);
        if (file_handle_ != INVALID_HANDLE_VALUE) CloseHandle(file_handle_);
#else
        if (base_ptr_ && base_ptr_ != MAP_FAILED) munmap(base_ptr_, max_size_);
        if (fd_ >= 0) close(fd_);
#endif
    }

    std::string filepath_;
    size_t max_size_;
    size_t write_offset_;
    uint64_t sequence_counter_;
    char* base_ptr_{nullptr};

#if defined(_WIN32)
    HANDLE file_handle_{INVALID_HANDLE_VALUE};
    HANDLE mapping_handle_{NULL};
#else
    int fd_{-1};
#endif
};

} // namespace lob
