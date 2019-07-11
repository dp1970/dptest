import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE","managerment_system.settings")
    import django
    django.setup()
    import random
    from app01 import models
    li = []
    for i in range(1,101):
        obj = models.Customer(
            qq = "".join([str(i) for i in random.choices(range(1,10),k=11)]),
            name = "dp"+str(i),
            sex = random.choice(["male","female"]),
            source = random.choice(["referral","baidu_ads","public_class","website_luffy"]),
            course= random.choice(['LinuxL','PythonFullStack'])
        )
        li.append(obj)
    models.Customer.objects.bulk_create(li)