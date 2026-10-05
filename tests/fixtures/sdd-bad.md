# Broken — Thiết kế hệ thống

## 1. Giới thiệu

### 1.1 Bối cảnh

Xem mục 3.2 và mục 1.1, 1.3.

## 3. Sai số thứ tự

### 3.1 A

| Mã | Yêu cầu |
| --- | --- |
| FR-01 | a, xem FR-02 |
| FR-01 | trùng |

### 3.3 B

```mermaid
flowchart LR
    A[Giữ vé (SKIP LOCKED)] --> B["ok (x)"]
```

```sql
SELECT 1;
