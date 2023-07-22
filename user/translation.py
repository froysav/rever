from modeltranslation.translator import register, TranslationOptions

from user.models import Project


@register(Project)
class ProjectTranslationOption(TranslationOptions):
    fields = ('title', 'description', 'keyword')