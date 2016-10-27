from cassandra.cqlengine import columns, ValidationError
from cassandra.cqlengine.models import Model
from uuid import uuid4
from datetime import datetime

class Activity(Model):
  """Keeps track of all events in the questionnaire frontend."""
  id = columns.UUID(default=uuid4)
  user_id = columns.UUID(primary_key=True)
  element_name = columns.Text()
  element_value = columns.Text()
  # We want the partition key to be the user_id, while the clustering_key should
  # be the change_datetime, if we want the data to be ordered from newest to
  # oldest
  change_datetime = columns.DateTime(
    default=datetime.now(),
    primary_key=True,
    clustering_order='DESC'
  )


class Questionnaire(Model):
  """Keeps track of a specific questionnaire answers."""

  vim_emacs_choices = ('vim', 'emacs')
  compiled_interpreted_choices = ('compiled', 'interpreted')
  ide_texteditor_choices = ('ide', 'text_editor')
  marry_kiss_kill_keys_choices = ('marry', 'kiss', 'kill')
  java_net_choices = ('java', 'net')

  id = columns.UUID(primary_key=True, default=uuid4)
  user_id = columns.UUID(primary_key=True)
  name = columns.Text()
  vim_emacs = columns.Text()
  ide_texteditor = columns.Text()
  compiled_interpreted = columns.Text()
  favorite_ide = columns.Text()
  marry_kiss_kill = columns.Map(columns.Text, columns.Text)
  java_net = columns.Text()
  cloud_providers = columns.List(columns.Text)
  team_size = columns.SmallInt()
  preferred_location = columns.Text()

  def validate(self):
    super(Questionnaire, self).validate()
    if self.vim_emacs not in self.vim_emacs_choices:
      raise ValidationError('%s is not a valid choice for Vim/Emacs' % (
        self.vim_emacs))
    if self.compiled_interpreted not in self.compiled_interpreted_choices:
      raise ValidationError(
        '%s is not a valid choice for Compiled/Interpreted' % (
        self.compiled_interpreted))
    if self.ide_texteditor not in self.ide_texteditor_choices:
      raise ValidationError('%s is not a valid choice for IDE/Text Editor' % (
        self.ide_texteditor))
    if self.java_net not in self.java_net_choices:
      raise ValidationError('%s is not a valid choice for Java/.NET' % (
        self.java_net))