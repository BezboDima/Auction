# Generated by Django 4.0.5 on 2022-12-30 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting_comments_bids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='start_bid',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='start_bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]