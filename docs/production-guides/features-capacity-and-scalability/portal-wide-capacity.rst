Portal-Wide Capacity (`spec.portal.sessions.maximum`)
=====================================================

پارامتر `maximum` در `spec.portal.sessions` یک ظرفیت سراسری است  
تا مجموع کل sessionهای فعال (WorkshopSession) در Portal از یک مقدار مشخص بیشتر نشود.

**رفتار:** اگر به سقف maximum برسیم session جدید ساخته نمی‌شود و کاربر باید منتظر آزاد شدن ظرفیت بماند.

**نمونه yaml:**
.. code-block:: yaml

   spec:
     portal:
       sessions:
         maximum: 100

**نکته طراحی:**  
اگر چند workshop داری، برای هرکدام capacity اختصاصی تعریف کن تا یک ورکشاپ خاص تمام ظرفیت Portal را نگیره.

**Use Case:**  
مثلاً در رویداد ۳۰۰ نفره که فقط برای ۱۰۰ نفر زیرساخت داری، maximum را ۱۰۰ می‌گذاری و باقی منتظر capacity می‌مانند.
