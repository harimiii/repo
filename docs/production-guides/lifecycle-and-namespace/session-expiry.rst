Session Expiry (`spec.workshops[].expires`)
===========================================

پارامتر **expires** مشخص می‌کند سشن هر کاربر در هر ورکشاپ چه مدت بعد از فعال شدن خودکار حذف شود  
و منابع پس از آن آزاد می‌شود.

**نمونه yaml:**
.. code-block:: yaml

   spec:
     workshops:
       - name: terraform-intro
         capacity: 40
         reserved: 2
         expires: 45m

**Use Case:**  
اگر ورکشاپ‌های کوتاه‌مدت داری (مثلاً lab آموزشی ۴۵ دقیقه)، می‌توانی با expires ظرفیت را پس از اتمام session برای کاربر جدید آزاد کنی.
