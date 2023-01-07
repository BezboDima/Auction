# Generated by Django 4.0.5 on 2023-01-06 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_start_bid_auctionlisting_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(choices=[('Other', 'Other'), ('Potions', 'Potions'), ('Magic', 'Magic'), ('Houses', 'Houses'), ('Pets', 'Pets')], default='N/A', max_length=20),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='discription',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='comments',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auctionlisting'),
        ),
    ]
