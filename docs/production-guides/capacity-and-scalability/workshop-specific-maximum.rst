Workshop-Specific Maximum (`spec.workshops[].capacity`)
======================================================

پارامتر `capacity` در آرایه `spec.workshops[]`  
سقف تعداد جلسه همزمان (sessions) یک ورکشاپ خاص را تعیین می‌کند—مستقل از سایر workshopها.

**رفتار:**  
اگر سشن‌های یک ورکشاپ به capacity برسد:
- فقط آن ورکشاپ session جدید نمی‌پذیرد.
- بقیه workshopها فعال هستند (تا زمانی که سقف کل Portal پر نشده است).

**نمونه yaml:**
.. code-block:: yaml

   spec:
     portal:
       sessions:
         maximum: 100
     workshops:
       - name: k8s-basics
         capacity: 30

**سناریو:**  
در پورتال چند workshop نگذاریم همه منابع توسط یک ورکشاپ محبوب مصرف شود و توزیع منابع متعادل است.
