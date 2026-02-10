Reserved Pool (`spec.workshops[].reserved` و `spec.workshops[].initial`)
=======================================================================

Educates می‌تواند تعدادی session را به حالت warm standby نگه دارد  
تا کاربر بدون انتظار وارد شود:

- `reserved`: سشن‌های standby  
- `initial`: نمونه‌هایی که ابتدای رویداد pre-create می‌شوند

**رفتار:**
- Pods و Namespace قبل از ورود کاربر بالا می‌آیند؛ latency ورود پایین می‌آید.
- مجموع (reserved + active) هر ورکشاپ از capacity آن بیشتر نمی‌شود.

**نمونه yaml:**
.. code-block:: yaml

   spec:
     portal:
       sessions:
         maximum: 100
     workshops:
       - name: lab-kubernetes-fundamentals
         capacity: 100
         initial: 75
         reserved: 5

**نکته:**  
استفاده از reserved عالی است برای دموها و تجربه ورود فوری کاربر؛  
اما باعث افزایش مصرف منابع (و هزینه) خواهد شد.
