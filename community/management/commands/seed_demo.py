"""Seed the database with demo content so the site looks alive on first deploy.
Run:  python manage.py seed_demo
Safe to run multiple times — it clears and re-creates demo rows.
"""
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from community.models import Event, Activity, FAQ, SiteStat, ActivityType


class Command(BaseCommand):
    help = "Örnek içerik oluşturur (etkinlik, aktivite, SSS, istatistik)."

    def handle(self, *args, **opts):
        now = timezone.now()

        Event.objects.all().delete()
        Event.objects.bulk_create([
            Event(title="Cumartesi Koşusu", activity_type=ActivityType.RUN,
                  location="Sahil Parkı", start_time=now + timedelta(days=2, hours=1),
                  distance_km=6, level="Tüm seviyeler", participant_count=32, is_weekly=True),
            Event(title="Gündoğumu Yogası", activity_type=ActivityType.YOGA,
                  location="Botanik Bahçe", start_time=now + timedelta(days=4),
                  level="Tüm seviyeler", participant_count=18, is_weekly=True),
            Event(title="Yayla Yürüyüşü", activity_type=ActivityType.HIKE,
                  location="Ayder", start_time=now + timedelta(days=9),
                  distance_km=12, level="Orta", participant_count=24),
        ])

        Activity.objects.all().delete()
        Activity.objects.bulk_create([
            Activity(title="Koşu", order=1, description="Haftalık grup koşuları ve tempo antrenmanları. İlk 1K'nı da atacaksın, maratonuna da hazırlanacaksın."),
            Activity(title="Yoga", order=2, description="Doğada gündoğumu seansları. Nefes, esneme ve toparlanma — koşunun ve haftanın dengeleyicisi."),
            Activity(title="Doğa Yürüyüşü", order=3, description="Yayla rotaları ve zirve tırmanışları. Kaçkar'ın patikalarını rehberli, güvenli ve birlikte keşfet."),
        ])

        FAQ.objects.all().delete()
        FAQ.objects.bulk_create([
            FAQ(order=1, question="Katılmak için deneyimli olmam gerekiyor mu?",
                answer="Hayır. Etkinliklerimiz her seviyeye açık. İlk kez koşacaksan da, yıllardır spor yapıyorsan da sana uygun bir grup ve tempo var."),
            FAQ(order=2, question="Üyelik ücretli mi?",
                answer="Düzenli buluşmalarımız ücretsiz ve herkese açık. Bazı özel etkinlikler için sembolik bir katkı payı olabilir."),
            FAQ(order=3, question="Buluşmalar nereden başlıyor?",
                answer="Her etkinliğin başlangıç noktası takvim kartında yazıyor. Kayıt olduğunda buluşma detaylarını iletiyoruz."),
            FAQ(order=4, question="Yanımda ne getirmeliyim?",
                answer="Rahat kıyafet, su ve pozitif enerji. Doğa yürüyüşleri için uygun ayakkabı öneririz."),
        ])

        SiteStat.objects.all().delete()
        SiteStat.objects.bulk_create([
            SiteStat(order=1, number="200+", key="Topluluk", text="Aktif üye ve büyüyen bir aile"),
            SiteStat(order=2, number="3", key="Aktivite", text="Koşu · Yoga · Doğa yürüyüşü"),
            SiteStat(order=3, number="Haftada 4", key="Buluşma", text="Düzenli, ücretsiz ve herkese açık"),
            SiteStat(order=4, number="2024", key="Kuruluş", text="İlk günden beri aynı ruhla"),
        ])

        self.stdout.write(self.style.SUCCESS("✓ Örnek içerik oluşturuldu."))
