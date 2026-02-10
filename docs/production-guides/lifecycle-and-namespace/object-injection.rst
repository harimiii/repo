Object Injection (`spec.session.objects`)
=========================================

با این گزینه می‌توانید هر resource دلخواه (مثل Secret, ConfigMap, Deployment) را در ابتدای هر سشن به شکل خودکار در Namespace شخصی کاربر inject کنید.

**موارد رایج:**
- ConfigMap
- Secret
- Deployment
- ServiceAccount

**نمونه yaml:**
.. code-block:: yaml

   spec:
     session:
       objects:
         - apiVersion: v1
           kind: Secret
           metadata:
             name: some-secret
           stringData:
             key: value
         - apiVersion: v1
           kind: ConfigMap
           metadata:
             name: config
           data:
             foo: "bar"

**کاربرد:** اجرای یک workshop که برای همه دانشجویان باید یک Secret یا ConfigMap مشترک یا اختصاصی قبل از شروع session تعریف شود.
