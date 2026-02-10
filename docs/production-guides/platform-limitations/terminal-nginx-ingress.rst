ناسازگاری ترمینال با Nginx Ingress
==================================
محدودیت:
Nginx می‌تواند در تغییرات مکرر کانفیگ باعث قطع WebSocketها شود (مثلاً هنگام reload/reconfigure).
الزام/راهکار:
استفاده از Contour به‌عنوان Ingress Controller توصیه می‌شود.

