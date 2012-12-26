from django.core.management.base import BaseCommand, CommandError
from mysite.settings import PROJECT_PATH
from essays.models import Essay, Category
import os, glob
import datetime

class Command(BaseCommand):
    args = 'None'
    help = '''Takes essays directory and refreshes Category/Essay objects
            in database.'''

    def handle(self, *args, **options):
        proceed = ''
        while proceed not in ('Y', 'N'):
            proceed = raw_input('This will clear existing Essays, Categories, and LegacyRedirects before recompiling them. Proceed? (Y/N)')

        if proceed == 'N':
            raise CommandError('Aborting')

        Essay.objects.all().delete()
        Category.objects.all().delete()
        
        os.chdir(os.path.join(PROJECT_PATH, 'essays', 'essays'))
        category_names = [f for f in os.listdir('.') if os.path.isdir(f)]

        for c in category_names:
            self.stdout.write('Browsing %s directory\n' % c)
            self.stdout.write('Processing essays...\n')
            os.chdir(c)
            new_category = Category(name=c)
            new_category.save()
            
            for essay in glob.glob('*.txt'):
                (essay_shortname, extension) = os.path.splitext(essay)
                self.stdout.write('%s\n' % essay_shortname)

                with open(essay) as f:
                    first_line = f.readline().rstrip('\n')
                    try:
                        legacy_id = int(first_line)
                        essay_longname = f.readline().rstrip('\n')
                        self.stdout.write('%s\n' % legacy_id)
                        self.stdout.write('%s\n' % essay_longname)
                    except ValueError:
                        legacy_id = None
                        essay_longname = first_line
                    finally:
                        essay_date= f.readline().rstrip('\n')
                        self.stdout.write('%s\n' % essay_date)
                        f.readline()
                        essay_content = unicode(f.read())
                essay_date = datetime.date(*map(int, essay_date.split('/')))
                new_essay = Essay(title = essay_longname,
                                  slug = essay_shortname,
                                  content = essay_content,
                                  category = new_category,
                                  date_written = essay_date,
                                  legacy_redirect = legacy_id)
                new_essay.save()
                                
            os.chdir('..')
        self.stdout.write('Done!\n')
                    