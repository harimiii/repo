Secret Injection & Propagation (SecretCopier/SecretExporter/SecretImporter/SecretInjector)
=========================================================================================
توضیح فنی:
برای انتقال امن Secret از Namespace مرکزی به سشن‌ها:


SecretExporter می‌تواند Secret را export کند.

SecretImporter در Namespace مقصد (سشن) با handshake و sharedSecret اجازه دریافت می‌دهد.

SecretCopier برای کپی‌های کنترل‌شده بین Namespaceها استفاده می‌شود.

SecretInjector برای تزریق image pull secret به ServiceAccountها کاربرد دارد.

Use Case:
در ورکشاپ‌هایی که نیاز به Registry خصوصی یا Git خصوصی دارند.
در این سناریو:

Secretها به‌صورت کنترل‌شده کپی می‌شوند.
کاربران به Secret اصلی دسترسی ندارند.
ریسک نشت اطلاعات کاهش می‌یابد.


