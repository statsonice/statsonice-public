from django.db import models
from statsonice.models.models_validator import EnumValidator

class Category(models.Model):
    CATEGORY_CHOICES = (
        ('MEN', 'Men'),
        ('LADIES', 'Ladies'),
        ('PAIRS', 'Pairs'),
        ('DANCE', 'Ice Dance'),
    )
    category = models.CharField(max_length = 10,
                                choices = CATEGORY_CHOICES,
                                default = '',
                                primary_key=True)

    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Category %s)' % (self.category)
    def clean(self):
        EnumValidator.validate_enum(self.category, Category.CATEGORY_CHOICES)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Category, self).save(*args, **kwargs)


class Component(models.Model):
    COMPONENT_CHOICES = (
        ('SS', 'Skating Skills'),
        ('TR', 'Transitions Transition/Linking Footwork Transition / Linking Footwork Transitions/Linking Footwork/Movements'),   # Transitions/Linking Footwork
        ('PE', 'Performance/Execution Performance / Execution'),  # Performance/Execution
        ('PF', 'Performance'),
        ('CH', 'Choreography/Composition Choreography / Composition Composition/Choreography Composition / Choreography'), # Choreography/Composition
        ('IN', 'Interpretation / Interpretation of the music'),
        ('CC', 'Choreography'),
        ('IT', 'Interpretation/Timing Interpretation / Timing'),
        ('TI', 'Timing'),
        ('MO', 'Footwork/Movement Footwork / Movement Footwork/Movements Footwork / Movements Linking Footwork/Movement Linking Footwork / Movement'),
    )
    component = models.CharField(max_length = 10,
                                 choices = COMPONENT_CHOICES,
                                 default = '',
                                 primary_key=True)
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Component %s)' % (self.component)
    def clean(self):
        EnumValidator.validate_enum(self.component, Component.COMPONENT_CHOICES)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Component, self).save(*args, **kwargs)


class Flag(models.Model):
    FLAG_CHOICES = (
        ('OL', 'Outlier'),
        ('PC', 'Perfect Consensus'),
        ('NC', 'No Consensus'),
        ('TO', 'Three and One')
    )

    flag = models.CharField(max_length = 2,
                            choices = FLAG_CHOICES,
                            default = 'NC',
                            primary_key = True)

    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Flag %s)' % (self.flag)

    # TODO: add clean and save methods, and validators


class Level(models.Model):
    LEVEL_CHOICES = (
        ('', ''),
        ('NO', 'No Test'),
        ('PP', 'Pre-Preliminary'),
        ('PR', 'Preliminary'),
        ('PJ', 'Pre-Juvenile'),
        ('JUV', 'Juvenile'),
        ('INT', 'Intermediate'),
        ('NOV', 'Novice'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    )
    level = models.CharField(max_length = 10,
                             choices = LEVEL_CHOICES,
                             default = '',
                             primary_key=True,
                             blank=True)

    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Level %s)' % (self.level)
    def clean(self):
        EnumValidator.validate_enum(self.level, Level.LEVEL_CHOICES)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Level, self).save(*args, **kwargs)


# TODO: resolve fact that definition of < changed
# before October 2010 < changed base value from triple to double, e.g.
# After October 2010, < replaced by <<
# After October 2010, < makes jumps worth 70% of base value
class Modifier(models.Model):
    MODIFIES_ONE = (
        ('<', 'Under-rotated jump'),
        ('<<', 'Downgraded jump'),
    )
    MODIFIES_AFTER = (
        ('SEQ', 'Jump sequence'),
        ('COMBO', 'Invalid combination'),
        ('TRANS', 'Dance Transition'),
        ('kpNNN', 'Key Point - NO, NO, NO'),
        ('kpYNN', 'Key Point - YES, NO, NO'),
        ('kpNYN', 'Key Point - NO, YES, NO'),
        ('kpNNY', 'Key Point - NO, NO, YES'),
        ('kpYYN', 'Key Point - YES, YES, NO'),
        ('kpYNY', 'Key Point - YES, NO, YES'),
        ('kpNYY', 'Key Point - NO, YES, YES'),
        ('kpYYY', 'Key Point - YES, YES, YES'),
        ('kpYTT', 'Key Point - YES, NO, NO'),
        ('kpTYT', 'Key Point - NO, YES, NO'),
        ('kpTTY', 'Key Point - NO, NO, YES'),
        ('kpYYT', 'Key Point - YES, YES, NO'),
        ('kpYTY', 'Key Point - YES, NO, YES'),
        ('kpTYY', 'Key Point - NO, YES, YES'),
        ('kpTNN', 'Key Point - YES, NO, NO'),
        ('kpNTN', 'Key Point - NO, YES, NO'),
        ('kpNNT', 'Key Point - NO, NO, YES'),
        ('kpTTN', 'Key Point - YES, YES, NO'),
        ('kpTNT', 'Key Point - YES, NO, YES'),
        ('kpNTT', 'Key Point - NO, YES, YES'),
        ('kpTTT', 'Key Point - YES, YES, YES'),
        ('kpTNY', 'Key Point - YES, NO, YES'),
        ('kpTYN', 'Key Point - NO, YES, YES'),
        ('kpNYT', 'Key Point - YES, YES, YES'),
        ('kpNTY', 'Key Point - YES, NO, YES'),
        ('kpYTN', 'Key Point - NO, YES, YES'),
        ('kpTNY', 'Key Point - YES, YES, YES'),
    )

    MODIFIES_ALL = (
        ('*', 'Invalid element'),
        ('!', 'Jump take off with wrong edge (short)'),
        ('e', 'Jump take off with wrong edge'),
        ('x', 'Credit for highlight distribution'),
    )

    MODIFIER_CHOICES = MODIFIES_ONE + MODIFIES_AFTER + MODIFIES_ALL

    modifier = models.CharField(max_length = 10,
                                choices = MODIFIER_CHOICES,
                                default = '',
                                primary_key=True)
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Modifier %s)' % (self.modifier)
    def clean(self):
        EnumValidator.validate_enum(self.modifier, Modifier.MODIFIER_CHOICES)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Modifier, self).save(*args, **kwargs)



class Segment(models.Model):
    SEGMENT_CHOICES = (
        ('', ''),
        ('SP', 'Short Program'),
        ('FS', 'Free Skating'),
        ('CD', 'Compulsory Dance'),
        ('OD', 'Original Dance'),
        ('FD', 'Free Dance'),
        ('SD', 'Short Dance'),
    )
    segment = models.CharField(max_length = 10,
                               choices = SEGMENT_CHOICES,
                               default = '',
                               primary_key=True,
                               blank=True)
    class Meta:
        app_label = 'statsonice'
    def __unicode__(self):
        return u'(Segment %s)' % (self.segment)
    def clean(self):
        EnumValidator.validate_enum(self.segment, Segment.SEGMENT_CHOICES)
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Segment, self).save(*args, **kwargs)

