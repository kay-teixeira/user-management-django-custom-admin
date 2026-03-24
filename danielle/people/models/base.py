from django.db import models
from django.utils import timezone

class ActiveQuerySet(models.QuerySet):
    """Intercepta exclusões em lote (bulk delete) do Django Admin."""
    def delete(self):
        return self.update(is_deleted=True, deleted_at=timezone.now())

class ActiveManager(models.Manager):
    """Manager customizado que retorna apenas registros não deletados."""
    def get_queryset(self):
        return ActiveQuerySet(self.model, using=self._db).filter(is_deleted=False)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    is_deleted = models.BooleanField(default=False, verbose_name="Deletado?")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Deletado em")

    objects = ActiveManager() 
    all_objects = models.Manager() 

    @property
    def formatted_created_at(self):
        return self.created_at.strftime("%d/%m/%Y")

    @property
    def formatted_updated_at(self):
        return self.updated_at.strftime("%d/%m/%Y")

    def delete(self, *args, **kwargs):
        """Intercepta exclusão de um único objeto."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, *args, **kwargs):
        super(BaseModel, self).delete(*args, **kwargs)

    class Meta:
        abstract = True