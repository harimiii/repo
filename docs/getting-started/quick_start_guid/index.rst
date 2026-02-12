.. _quick-start-guide:

راهنمای شروع سریع
==================

سریع‌ترین روش برای نصب و شروع کار با Educates این است که آن را روی سیستم محلی خود و با استفاده از یک Kubernetes cluster که توسط Kind ایجاد می‌شود اجرا کنید.

برای ساده‌تر شدن این فرآیند، Educates یک ابزار خط فرمان به نام ``educates`` CLI ارائه می‌دهد که می‌توانید با آن:

- یک Kubernetes cluster ایجاد کنید
- Educates را Deploy کنید
- Workshopها را Deploy و مدیریت کنید

این محیط محلی Educates همچنین بهترین گزینه برای توسعه محتوای Workshop شخصی شماست، زیرا شامل یک local image registry است که می‌تواند برای نگهداری:

- custom workshop base images
- Workshopهای منتشرشده شما

استفاده شود.

این ترکیب یک workflow سریع و محلی برای اعمال تغییرات روی Workshop فراهم می‌کند، بدون نیاز به انتشار در سرویس‌های ثالث.

توضیحات کامل نصب Educates روی هر Kubernetes cluster در بخش‌های بعدی مستندات ارائه شده است.

--------------------------------------------------------------------

نیازمندی‌های سیستم میزبان
--------------------------

برای Deploy کردن Educates روی سیستم محلی با استفاده از CLI، موارد زیر لازم است:

* باید از macOS یا Linux استفاده کنید. در Windows باید از WSL (Windows Subsystem for Linux) استفاده شود. CLI بیشتر روی macOS تست شده است.
* باید یک محیط ``docker`` فعال داشته باشید. این ابزار عمدتاً با Docker Desktop تست شده اما در macOS می‌توان از Colima نیز استفاده کرد.
* باید حافظه و فضای دیسک کافی به docker اختصاص داده باشید.
* نباید یک Kubernetes cluster مبتنی بر Kind از قبل در حال اجرا باشد.
* پورت‌های 80 (HTTP) و 443 (HTTPS) نباید روی سیستم شما استفاده شده باشند.
* در macOS برای استفاده از local DNS resolver باید پورت 53 آزاد باشد.
* پورت 5001 باید آزاد باشد زیرا برای local image registry استفاده می‌شود.

اگر از Docker Desktop استفاده می‌کنید باید:

* Allow the default Docker socket فعال باشد.
* Allow privileged port mapping فعال باشد.
* بسته به نسخه Docker Desktop ممکن است نیاز به فعال/غیرفعال کردن:
  Use kernel networking for UDP داشته باشید.

اگر از Colima استفاده می‌کنید، باید در فایل تنظیمات Educates این موارد را اضافه کنید:

::

  $ educates local config edit
  localKindCluster:
    listenAddress: 0.0.0.0

--------------------------------------------------------------------

دانلود CLI
-----------

برای دانلود Educates CLI به صفحه Releases مراجعه کنید:

https://github.com/educates/educates-training-platform/releases

آخرین نسخه را انتخاب کرده و فایل مناسب سیستم خود را دانلود کنید:

* educates-linux-amd64
* educates-linux-arm64
* educates-darwin-amd64
* educates-darwin-arm64

فایل دانلود شده را به ``educates`` تغییر نام دهید، آن را executable کنید:

::

  chmod +x educates

و در مسیر PATH سیستم قرار دهید.

برای دانلود مستقیم با curl:

Linux (amd64):

::

  curl -o educates -sL https://github.com/educates/educates-training-platform/releases/latest/download/educates-linux-amd64 && chmod +x educates

Linux (arm64):

::

  curl -o educates -sL https://github.com/educates/educates-training-platform/releases/latest/download/educates-linux-arm64 && chmod +x educates

macOS (amd64):

::

  curl -o educates -sL https://github.com/educates/educates-training-platform/releases/latest/download/educates-darwin-amd64 && chmod +x educates

macOS (arm64):

::

  curl -o educates -sL https://github.com/educates/educates-training-platform/releases/latest/download/educates-darwin-arm64 && chmod +x educates

در macOS نسخه‌ها sign نشده‌اند و باید به سیستم اجازه اجرای آن را بدهید.

همچنین می‌توان CLI را به صورت OCI image با استفاده از imgpkg دریافت کرد:

::

  imgpkg pull -i ghcr.io/educates/educates-client-programs:X.Y.Z -o educates-client-programs

--------------------------------------------------------------------

دامنه پیش‌فرض Ingress
----------------------

Educates برای Kubernetes Ingress به یک FQDN معتبر نیاز دارد.

به طور پیش‌فرض، CLI از دامنه nip.io بر اساس IP سیستم شما استفاده می‌کند:

مثال:

::

  192-168-1-10.nip.io

برخی قابلیت‌ها نیاز به wildcard TLS certificate دارند که برای nip.io قابل تولید با LetsEncrypt نیست.

همچنین برخی روترهای خانگی به دلیل DNS rebinding protection ممکن است nip.io را مسدود کنند.

در این راهنمای اولیه از nip.io استفاده می‌کنیم. تنظیم دامنه سفارشی و TLS در بخش‌های بعدی توضیح داده می‌شود.

--------------------------------------------------------------------

ایجاد Kubernetes cluster محلی
------------------------------

برای ایجاد cluster با Kind و Deploy کردن Educates:

::

  educates create-cluster

این دستور:

* Kubernetes cluster را ایجاد می‌کند
* security policy engine را فعال می‌کند
* Contour ingress controller را نصب می‌کند
* local image registry روی پورت 5001 راه‌اندازی می‌کند
* Educates را Deploy می‌کند

این فرآیند ممکن است تا ۵ دقیقه طول بکشد.

پس از اتمام، context جدید با نام:

::

  kind-educates

در kubeconfig شما اضافه می‌شود.

--------------------------------------------------------------------

Deploy کردن یک Workshop
------------------------

برای Deploy کردن یک Workshop نمونه:

::

  educates deploy-workshop -f https://github.com/educates/lab-k8s-fundamentals/releases/latest/download/workshop.yaml

اگر Training Portal فعال نباشد، به صورت خودکار Deploy می‌شود.

--------------------------------------------------------------------

دسترسی به Workshop
-------------------

برای باز کردن Training Portal:

::

  educates browse-workshops

برای دیدن URL:

::

  educates list-portals

برای دیدن password:

::

  educates view-credentials

بار اول ممکن است به دلیل Pull شدن image کمی زمان ببرد.

--------------------------------------------------------------------

حذف Workshop
------------

برای حذف Workshop:

::

  educates delete-workshop -f https://github.com/educates/lab-k8s-fundamentals/releases/latest/download/workshop.yaml

یا با نام:

::

  educates delete-workshop -n workshop-name
