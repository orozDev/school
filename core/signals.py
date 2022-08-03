
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.core.mail import send_mail
from .models import Teacher, Student
from school.settings import EMAIL_HOST_USER


@receiver(post_save, sender=Teacher)
def post_save_teacher_avatar(instance, created, **kwargs):
    try:
        image = Image.open(instance.avatar)
        if image.height != image.width:
            if image.height < image.width:
                x = (int(image.width) - int(image.height)) / 2
                y = 0
                h = image.height
                w = image.height
                
            elif image.height > image.width:
                y = (int(image.height) - int(image.width)) / 2
                x = 0
                h = image.width
                w = image.width
            
            cropped_image = image.crop((x, y, w, h))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            resized_image.save(instance.avatar.path)
    except Exception:
        pass


@receiver(post_save, sender=Teacher)
def post_save_teacher(instance, created, **kwargs):
    if created:
        try: 
            group = instance.group
            group.teacher = instance
            group.save()
        except Exception:
            pass


@receiver(post_save, sender=Student)
def post_save_student(instance, created, **kwargs):
    if created:
        group = instance.group
        group.students.add(instance)
        group.save()


@receiver(post_save, sender=Student)
def post_save_student_to_send_message(instance, created, **kwargs):
    if created:
        result = send_mail(
            f'{instance.name} !',
            f'Учитель(ца) {instance.group.teacher.name} добавил вас в список учеников',
            EMAIL_HOST_USER,
            [instance.email],
            fail_silently=True,
        )
        if result:
            instance.is_active = True
            instance.save()
    

        