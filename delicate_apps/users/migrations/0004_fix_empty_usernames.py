from django.db import migrations

def fix_empty_usernames(apps, schema_editor):
    User = apps.get_model('users', 'User')
    users_with_empty_username = User.objects.filter(username='')
    
    for user in users_with_empty_username:
        base_username = user.email.split('@')[0]
        username = base_username
        count = 1
        
        # Buscar un username único
        while User.objects.filter(username=username).exists() and username != '':
            username = f"{base_username}{count}"
            count += 1
        
        user.username = username
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_managers'), 
    ]

    operations = [
        migrations.RunPython(fix_empty_usernames),
    ]