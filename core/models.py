from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models


class TelegramUser(models.Model):
    uid = models.BigIntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    chat = models.ForeignKey("TelegramChat", on_delete=models.CASCADE)

    def full_name(self):
        return f"{self.first_name}{'' if self.last_name is None else ' ' + self.last_name}"

    def __str__(self):
        return f'{self.pk} {self.full_name()}'


class TelegramChat(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    type = models.CharField(max_length=20, default='private')
    name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    state = models.TextField(default='init')
    state_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.type} chat {self.title or self.username or (self.first_name + self.last_name)}"


class TelegramMessage(models.Model):
    message_id = models.BigIntegerField()
    from_user = models.ForeignKey(TelegramUser, null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='%(class)s_from_user')
    date = models.DateTimeField()
    edit_date = models.DateTimeField(null=True, blank=True)
    chat = models.ForeignKey(TelegramChat, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    new_chat_members = models.ManyToManyField(TelegramUser, related_name='%(class)s_new_chat_members')

    def __str__(self):
        return f"{self.from_user.full_name()} in {self.chat}: {self.text}"


class TelegramUpdate(models.Model):
    update_id = models.BigIntegerField(unique=True)
    message = models.ForeignKey(TelegramMessage, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='%(class)s_message')
    edited_message = models.ForeignKey(TelegramMessage, null=True, blank=True, on_delete=models.CASCADE,
                                       related_name='%(class)s_edited_message')
    effective_message = models.ForeignKey(TelegramMessage, null=True, blank=True, on_delete=models.CASCADE,
                                          related_name='%(class)s_effective_message')
    effective_chat = models.ForeignKey(TelegramChat, null=True, blank=True, on_delete=models.CASCADE)
    effective_user = models.ForeignKey(TelegramUser, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"from user {self.effective_user} to chat {self.effective_chat} with " \
            f"{'edited ' if self.edited_message is not None else ''}message {self.effective_message}"


class RCUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, telegram_uid, password, **extra_fields):
        if not telegram_uid:
            raise ValueError('telegram_uid needed for user creation')
        user = self.model(telegram_uid=telegram_uid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, telegram_uid, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(telegram_uid, password, **extra_fields)

    def create_superuser(self, telegram_uid, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(telegram_uid, password, **extra_fields)


class RCUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'telegram_uid'
    REQUIRED_FIELDS = []

    is_staff = models.BooleanField(default=False)

    telegram_user = models.ForeignKey(TelegramUser, null=True, on_delete=models.CASCADE)
    telegram_uid = models.TextField(unique=True)

    role = models.CharField(default="common", max_length=100)

    gang = models.ForeignKey('Gang', null=True, on_delete=models.CASCADE)  # TODO change to m2m
    tags = ArrayField(models.CharField(max_length=100), default=list)

    # is_regular = models.BooleanField(default=True)
    # is_active = models.BooleanField(default=True)

    objects = RCUserManager()

    def mention(self):
        return f'[{self.telegram_user.first_name}](tg://user?id={self.telegram_user.chat.chat_id})'

    def __str__(self):
        return f'{self.telegram_user.first_name if self.telegram_user is not None else "unknown"} {self.telegram_uid}'


class Gang(models.Model):
    token = models.CharField(max_length=10)
    default_times = ArrayField(models.TimeField(), default=list)


class SeparatorQuestion(models.Model):
    gang = models.ForeignKey(Gang, on_delete=models.CASCADE)
    text = models.TextField()
    variants = ArrayField(models.CharField(max_length=100))


class HistoryEntry(models.Model):
    user1 = models.ForeignKey(RCUser, on_delete=models.CASCADE, related_name='%(class)s_user1')
    user2 = models.ForeignKey(RCUser, on_delete=models.CASCADE, related_name='%(class)s_user2')
    ts = models.DateTimeField()
