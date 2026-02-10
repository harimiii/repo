تمدید کنترل‌شده زمان (`spec.workshops[].deadline`, `spec.workshops[].overtime`)
===============================================================================

برای سناریوهایی که زمان session محدود اما قابل تمدید است، باید همزمان **expires**، **deadline** و **overtime** را تنظیم کنی:

* **deadline**: کل زمان مجاز session (حتی با تمدید)
* **overtime**: مقدار زمان هر تمدید

**نمونه yaml:**
.. code-block:: yaml

   spec:
     workshops:
       - name: exam-lab
         expires: 60m
         overtime: 30m
         deadline: 120m

در این مثال، کاربر می‌تواند session را تا دو بار ۳۰ دقیقه‌ای تمدید کند اما مجموعاً از ۱۲۰ دقیقه بالاتر نمی‌رود.
