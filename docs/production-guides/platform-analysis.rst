# گزارش تحلیل فنی پلتفرم Educates (Enhanced + Use Case)

---

## ۱. ویژگی‌های ظرفیت و مقیاس‌پذیری  
این دسته برای کنترل مصرف منابع، جلوگیری از overload و مدیریت رویدادهای بزرگ (Workshop / Bootcamp / Exam) حیاتی است.

> نکته مهم: در نسخه‌های فعلی Educates، «limiter سراسری» معمولاً با `spec.portal.sessions.maximum` پیاده‌سازی می‌شود و برای هر ورکشاپ هم از `spec.workshops[].capacity / reserved / initial` استفاده می‌شود.

---

### Portal-Wide Capacity (`spec.portal.sessions.maximum`)

**تعریف در:** `TrainingPortal`

**توضیح فنی:**  
یک limiter سراسری در سطح کل پورتال که سقف تعداد `WorkshopSession`های همزمان را در مجموعِ همه ورکشاپ‌ها مشخص می‌کند. این کنترل باعث می‌شود مجموع سشن‌های فعال در کل پورتال از یک عدد مشخص بالاتر نرود.

**رفتار سیستم (Operational):**
- اگر ظرفیت کل پر شود، سشن جدید قابل ایجاد/اختصاص نیست.
- سیستم صف یا Waiting Room داخلی ندارد (برای تجربه بهتر باید از `reserved/initial` یا یک لایه بیرونی مثل Front-end استفاده شود).

**Use Case:**

در رویدادی با ۳۰۰ شرکت‌کننده، فقط زیرساخت برای ۱۰۰ سشن همزمان آماده است.  
در این سناریو:
- مقدار `maximum` روی **100** تنظیم می‌شود.
- از overload شدن کلاستر جلوگیری می‌شود.
- مصرف هزینه ابری قابل پیش‌بینی باقی می‌ماند.

**نمونه YAML:**
```yaml
spec:
  portal:
    sessions:
      maximum: 100
````

**نکات طراحی (پیشنهادی):**

* اگر چند ورکشاپ دارید، برای هر کدام `capacity` جدا تعیین کنید تا یک ورکشاپ کل ظرفیت را مصرف نکند.
* اگر پورتال را طولانی‌مدت باز نگه می‌دارید، در کنار ظرفیت از `expires` استفاده کنید تا ظرفیت در طول زمان آزاد شود.

---

### Workshop-Specific Maximum (`spec.workshops[].capacity`)

**تعریف در:** `TrainingPortal`

**توضیح فنی:**
سقف تعداد سشن‌های همزمان برای **یک ورکشاپ خاص**، مستقل از سایر ورکشاپ‌ها. این مقدار تعیین می‌کند آن ورکشاپ چند `WorkshopSession` همزمان می‌تواند داشته باشد.

**رفتار سیستم:**

* اگر یک ورکشاپ به `capacity` خودش برسد:

  * فقط همان ورکشاپ دیگر سشن جدید نمی‌گیرد.
  * بقیه ورکشاپ‌ها همچنان فعال می‌مانند (تا زمانی که سقف کل پورتال پر نشده باشد).

**Use Case:**

در پورتالی با چند ورکشاپ، نمی‌خواهیم یک ورکشاپ محبوب تمام ظرفیت را مصرف کند.
در این سناریو:

* برای هر ورکشاپ سقف جداگانه تعریف می‌شود.
* تعادل مصرف منابع حفظ می‌گردد.
* سایر ورکشاپ‌ها بدون اختلال در دسترس می‌مانند.

**نمونه YAML:**

```yaml
spec:
  portal:
    sessions:
      maximum: 100
  workshops:
  - name: k8s-basics
    capacity: 30
```

---

### Reserved Pool (`spec.workshops[].reserved` + `spec.workshops[].initial`)

**تعریف در:** `TrainingPortal`

**توضیح فنی:**
Educates می‌تواند تعدادی `WorkshopSession` را از قبل آماده (Warm) نگه دارد تا کاربر بدون انتظار وارد شود.

* `reserved`: تعداد سشن‌های standby (گرم و آماده).
* `initial`: تعداد سشن‌هایی که در شروع رویداد از قبل ایجاد می‌شوند (برای هجوم ورودی اولیه).

**رفتار سیستم:**

* Namespace و Podها از قبل بالا می‌آیند و latency ورود کمتر می‌شود.
* هزینه زیرساخت افزایش پیدا می‌کند چون منابع از قبل مصرف می‌شوند.
* مجموع سشن‌های (allocated + reserved) برای هر ورکشاپ از `capacity` آن بالاتر نمی‌رود.

**Use Case:**

در یک دمو زنده یا نمایشگاه فناوری که تجربه کاربری اولویت دارد.
در این سناریو:

* تعدادی سشن به‌صورت Warm نگه داشته می‌شوند.
* کاربران تقریباً بدون انتظار وارد محیط می‌شوند.
* افزایش هزینه به‌عنوان trade-off پذیرفته می‌شود.

**نمونه YAML:**

```yaml
spec:
  portal:
    sessions:
      maximum: 100
  workshops:
  - name: lab-kubernetes-fundamentals
    capacity: 100
    initial: 75
    reserved: 5
```

---

## ۲. ویژگی‌های چرخه حیات و مدیریت Namespace

این بخش ستون فقرات کنترل هزینه، پاک‌سازی خودکار و جلوگیری از اشغال دائمی ظرفیت است.

---

### Session Expiry (`spec.workshops[].expires`)

**تعریف در:** `TrainingPortal` (سطح هر ورکشاپ)

**توضیح فنی:**
پس از پایان زمان مشخص‌شده:

* `WorkshopSession` به‌صورت خودکار حذف می‌شود.
* در نتیجه Namespace و منابع آزاد می‌شوند.
* ظرفیت برای کاربران بعدی آزاد می‌گردد.

**Use Case:**

در یک ورکشاپ کوتاه Terraform برای تازه‌کارها.
در این سناریو:

* زمان هر سشن روی **۴۵ دقیقه** تنظیم می‌شود.
* پس از پایان زمان، سشن حذف می‌گردد.
* منابع برای کاربران بعدی آزاد می‌شوند.

**نمونه YAML:**

```yaml
spec:
  workshops:
  - name: terraform-intro
    capacity: 40
    reserved: 2
    expires: 45m
```

---

### Orphaned Session Cleanup (`spec.workshops[].orphaned`)

**تعریف در:** `TrainingPortal` (سطح هر ورکشاپ)

**توضیح فنی:**
برای سشن‌هایی که کاربر صفحه را بسته یا مدت طولانی inactive بوده است، می‌توان سشن‌های orphaned را terminate کرد تا ظرفیت قفل نشود.

**Use Case:**

در رویداد عمومی که کاربران زیادی سشن را باز می‌کنند و بدون خروج صحیح صفحه را می‌بندند.
در این سناریو:

* با `orphaned` ظرفیت سریع‌تر آزاد می‌شود.
* ریسک حذف ناخواسته سشن (مثلاً در sleep شدن لپ‌تاپ) باید در نظر گرفته شود.

**نمونه YAML:**

```yaml
spec:
  workshops:
  - name: public-workshop
    capacity: 80
    orphaned: 5m
```

---

### تمدید کنترل‌شده زمان (`spec.workshops[].deadline` + `spec.workshops[].overtime`)

**تعریف در:** `TrainingPortal`

**توضیح فنی:**
اگر `expires` دارید ولی می‌خواهید امکان تمدید محدود بدهید:

* `deadline` سقف نهایی زمان سشن را مشخص می‌کند.
* `overtime` مقدار افزایشی هر تمدید را تعیین می‌کند.

**Use Case:**

در آزمون عملی (Exam) با زمان پایه ۶۰ دقیقه، اما امکان تمدید مرحله‌ای تا سقف ۱۲۰ دقیقه.
در این سناریو:

* زمان پایه با `expires` کنترل می‌شود.
* تمدید با `overtime` انجام می‌شود.
* سقف نهایی با `deadline` محدود می‌شود.

---

### Resource Budget (`session.namespaces.budget` + `LimitRange`/`ResourceQuota`)

**تعریف در:** `Workshop` (`Workshop Definition`)

**توضیح فنی:**
برای کنترل منابع هر کاربر در Namespace سشن‌ها می‌توانید از `session.namespaces.budget` استفاده کنید:

* حالت‌های آماده مثل `small/medium/large` (سریع و ساده)
* یا حالت `custom` برای تزریق دقیق `LimitRange` و `ResourceQuota` از طریق `session.objects`

**رفتار سیستم:**

* اگر کاربر بیش از quota مصرف کند، Kubernetes خطای `Forbidden` می‌دهد.
* Educates معمولاً به‌صورت مستقیم مداخله نمی‌کند؛ این کنترل در لایه Kubernetes اعمال می‌شود.

**Use Case:**

در دوره دواپس پیشرفته که کاربران دسترسی کامل دارند و ممکن است اشتباهی workload سنگین اجرا کنند.
در این سناریو:

* مصرف منابع هر کاربر محدود می‌شود.
* خطاهای ناخواسته باعث آسیب به کل کلاستر نمی‌شوند.
* پایداری محیط حفظ می‌گردد.

**نمونه YAML (preset آماده):**

```yaml
spec:
  session:
    namespaces:
      budget: medium
```

**نمونه YAML (custom با تزریق `LimitRange`/`ResourceQuota` از طریق `session.objects`):**

```yaml
spec:
  session:
    namespaces:
      budget: custom
    objects:
    - apiVersion: v1
      kind: LimitRange
      metadata:
        name: limits
      spec:
        limits:
        - type: Container
          defaultRequest:
            cpu: 50m
            memory: 128Mi
          default:
            cpu: 500m
            memory: 512Mi
    - apiVersion: v1
      kind: ResourceQuota
      metadata:
        name: quota
      spec:
        hard:
          requests.cpu: "2"
          requests.memory: 4Gi
          limits.cpu: "2"
          limits.memory: 4Gi
          pods: "10"
```

---

### Object Injection (`spec.session.objects`)

**تعریف در:** `Workshop` (`Workshop Definition`)

**توضیح فنی:**
تزریق خودکار منابع Kubernetes هنگام ایجاد سشن (داخل Namespace مربوط به سشن). منابع رایج:

* ConfigMap
* Secret
* Deployment
* ServiceAccount

این کار باعث می‌شود محیط اولیه همه کاربران یکسان، استاندارد و قابل پیش‌بینی باشد.

**Use Case:**

در دوره GitOps که همه کاربران باید محیط اولیه یکسان داشته باشند.
در این سناریو:

* منابع پایه به‌صورت خودکار تزریق می‌شوند.
* تنظیمات دستی حذف می‌شود.
* محیط‌ها استاندارد و قابل پیش‌بینی هستند.

---

## ۳. امنیت و ایزولاسیون

---

### Policy Integration (Kyverno)

**توضیح فنی:**
با ادغام policy engine مثل Kyverno می‌توانید از پیکربندی‌های ناامن جلوگیری کنید (مثلاً محدود کردن privileged، جلوگیری از hostPath، یا enforce کردن best-practiceها).

**Use Case:**

در آموزش امنیت Kubernetes به کاربران ناشناس.
در این سناریو:

* YAMLهای ناامن مسدود می‌شوند.
* اجرای کانتینرهای privileged محدود/غیرفعال می‌شود.
* امنیت کلاستر حفظ می‌شود.

---

### Secret Injection & Propagation (`SecretCopier` / `SecretExporter` / `SecretImporter` / `SecretInjector`)

**توضیح فنی:**
برای انتقال امن Secret از Namespace مرکزی به سشن‌ها:

* `SecretExporter` می‌تواند Secret را export کند.
* `SecretImporter` در Namespace مقصد (سشن) با handshake و `sharedSecret` اجازه دریافت می‌دهد.
* `SecretCopier` برای کپی‌های کنترل‌شده بین Namespaceها استفاده می‌شود.
* `SecretInjector` برای تزریق image pull secret به ServiceAccountها کاربرد دارد.

**Use Case:**

در ورکشاپ‌هایی که نیاز به Registry خصوصی یا Git خصوصی دارند.
در این سناریو:

* Secretها به‌صورت کنترل‌شده کپی می‌شوند.
* کاربران به Secret اصلی دسترسی ندارند.
* ریسک نشت اطلاعات کاهش می‌یابد.

---

## ۴. ویژگی‌های کمتر دیده‌شده اما بسیار اثرگذار

---

### Container Runtime Class (`clusterRuntime.class`)

**توضیح فنی:**
می‌توانید runtime class را برای workloadهای سشن تغییر دهید (مثلاً Kata) تا ایزولاسیون قوی‌تر شود، مخصوصاً زمانی که کدهای untrusted اجرا می‌شوند.

**Use Case:**

در اجرای کدهای Untrusted یا آموزش Zero-Trust برای ایزولاسیون قوی‌تر.

---

### Shared OCI Image Cache (`oci_image_cache`)

**توضیح فنی:**
برای رویدادهای بزرگ با image مشترک، استفاده از cache باعث کاهش فشار pull و جلوگیری از throttling و همچنین سریع‌تر شدن شروع سشن‌ها می‌شود.

**Use Case:**

در رویدادهای بزرگ با image مشترک برای کاهش فشار روی registry و جلوگیری از rate limit.

---

### Examiner Feedback Loop (`session.applications.examiner`)

**توضیح فنی:**
با examiner می‌توانید ارزیابی خودکار وضعیت منابع و کارهای عملی را انجام دهید و feedback فوری بدهید.

**Use Case:**

در آزمون عملی Kubernetes برای ارزیابی خودکار وضعیت منابع.

---

### Dashboard Custom Tabs (`dashboard:open-url`)

**توضیح فنی:**
می‌توانید ابزارهایی مثل Grafana یا ArgoCD را به‌صورت یک tab داخل داشبورد آموزشی نمایش دهید تا کاربر در یک محیط یکپارچه کار کند.

**Use Case:**

به‌جای اینکه کاربر بین چند URL جابه‌جا شود، همه چیز داخل داشبورد آموزشی مجتمع می‌شود.

---

## ۵. محدودیت‌های فنی و چالش‌های عملیاتی

درک این محدودیت‌ها برای پایداری پلتفرم در مقیاس بزرگ ضروری است.

---

### ۱) ناسازگاری ترمینال با Nginx Ingress

**محدودیت:**
Nginx می‌تواند در تغییرات مکرر کانفیگ باعث قطع WebSocketها شود (مثلاً هنگام reload/reconfigure).

**الزام/راهکار:**
استفاده از **Contour** به‌عنوان Ingress Controller توصیه می‌شود.

---

### ۲) عدم وجود سیستم صف (No Queuing)

**محدودیت:**
Educates فاقد Waiting Room است.

**رفتار:**
در صورت پر شدن ظرفیت، کاربر معمولاً با خطا (مثل 404 یا 503) مواجه می‌شود.

**راهکار عملی:**

* مدیریت تجربه کاربری با `reserved/initial`
* یا استفاده از یک لایه بیرونی (Front-end) برای نمایش پیام مناسب و کنترل ورودی

---

### ۳) مشکل طول URL و گواهینامه SSL

**محدودیت/ریسک عملیاتی:**
طول hostname و ساختار نام‌گذاری می‌تواند در صدور TLS Certificate یا محدودیت‌های DNS مشکل ایجاد کند.

**راهکار:**

* کوتاه نگه داشتن نام‌ها (TrainingPortal/Workshop/Session)
* استفاده از wildcard DNS و (در صورت امکان) wildcard certificate
* پرهیز از نام‌گذاری‌های طولانی و نسخه‌دار در hostname عمومی

---

### ۴) ناسازگاری Safari با HTTP/2

**محدودیت:**
Safari ممکن است در برخی سناریوها با HTTP/2 اتصال را قطع کند.

**راهکار:**
غیرفعال کردن HTTP/2 در Ingress کلاستر (در صورت وجود کاربران Safari به‌صورت قابل توجه).

---

## ضمیمه: الگوهای پیشنهادی پیکربندی (Use Case محور)

### الگوی A: رویداد بزرگ با ورود موجی

* `spec.portal.sessions.maximum` مشخص (مثلاً 100)
* `initial` بالا (مثلاً 70–80٪ تعداد مورد انتظار)
* `reserved` کوچک ولی ثابت (مثلاً 5) برای late arrivals

### الگوی B: پورتال دائمی (Self-paced)

* `expires` برای آزادسازی ظرفیت در طول زمان
* `orphaned` فقط در صورتی که حذف ناخواسته مشکل‌ساز نشود
* `session.namespaces.budget` فعال (حداقل `small` یا `medium`)

### الگوی C: آزمون عملی

* `expires` + `deadline` (تمدید کنترل‌شده)
* `examiner` برای checkهای خودکار
* Kyverno برای جلوگیری از پیکربندی‌های ناامن

---

