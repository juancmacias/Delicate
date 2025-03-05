from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('users', '0002_alter_user_managers'),  # Cambiado para coincidir con tu estructura
    ]

    operations = [
        migrations.RunSQL(
            # SQL para eliminar la restricción de clave foránea existente
            """
            ALTER TABLE django_admin_log 
            DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;
            """,
            # SQL de reversión (opcional)
            """
            ALTER TABLE django_admin_log 
            ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id 
            FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;
            """
        ),
        migrations.RunSQL(
            # SQL para agregar la nueva restricción de clave foránea
            """
            ALTER TABLE django_admin_log 
            ADD CONSTRAINT django_admin_log_user_id_fk_users_user 
            FOREIGN KEY (user_id) REFERENCES users_user(id) DEFERRABLE INITIALLY DEFERRED;
            """,
            # SQL de reversión (opcional)
            """
            ALTER TABLE django_admin_log 
            DROP CONSTRAINT django_admin_log_user_id_fk_users_user;
            """
        ),
    ]