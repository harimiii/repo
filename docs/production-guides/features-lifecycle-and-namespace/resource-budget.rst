Resource Budget (`session.namespaces.budget` + `LimitRange`/`ResourceQuota`)
==========================================================================

برای کنترل منابع هر کاربر در Namespace مربوط به session می‌توان با پارامتر **budget** بودجه استاندارد تعیین کرد (small/medium/large).

**پیکربندی ساده:**
.. code-block:: yaml

   spec:
     session:
       namespaces:
         budget: medium

**پیکربندی سفارشی و پیشرفته:**
برای مدیریت دقیق منابع می‌توان LimitRange یا ResourceQuota دلخواه inject کرد:

.. code-block:: yaml

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

**کاربرد:** برای ادمین‌هایی که می‌خواهند جلوی misuse منابع توسط کاربران را بگیرند.
