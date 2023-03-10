# Generated by Django 4.0.5 on 2022-12-30 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_bids_start_bid_auctionlisting_start_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlisting',
            old_name='start_bid',
            new_name='price',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='anyBids',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bids',
            name='current',
            field=models.BooleanField(default=False),
        ),
    ]
