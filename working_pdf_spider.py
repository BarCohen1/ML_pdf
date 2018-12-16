import scrapy
import time
import os


CUR_PDF_PATH = "C:/Users/Bar/PycharmProjects/pdf_parser/pdfs"


class QuotesSpider(scrapy.Spider):
    counter = 0
    cur_m = ''
    name = "pdf"
    start_urls = ["http://personalcare.manualsonline.com/manuals/device/pacemaker.html", "http://personalcare.manualsonline.com/manuals/device/pedicure_spa.html", "http://personalcare.manualsonline.com/manuals/device/personal_lift.html","http://personalcare.manualsonline.com/manuals/device/pill_reminder_device.html","http://personalcare.manualsonline.com/manuals/device/respiratory_product.html","http://personalcare.manualsonline.com/manuals/device/scale.html","http://personalcare.manualsonline.com/manuals/device/skin_care_product.html","http://personalcare.manualsonline.com/manuals/device/sleep_apnea_machine.html","http://personalcare.manualsonline.com/manuals/device/styling_iron.html" ,"http://personalcare.manualsonline.com/manuals/device/ultrasonic_jewelry_cleaner.html", "http://personalcare.manualsonline.com/manuals/device/wheelchair.html","http://personalcare.manualsonline.com/manuals/device/thermometer.html","http://personalcare.manualsonline.com/manuals/device/oxygen_equipment.html","http://personalcare.manualsonline.com/manuals/device/mobility_aid.html","http://personalcare.manualsonline.com/manuals/device/mobility_scooter.html", "http://personalcare.manualsonline.com/manuals/device/nebulizer.html","http://personalcare.manualsonline.com/manuals/device/home_dialysis_equipment.html","http://personalcare.manualsonline.com/manuals/device/insulin_pen.html","http://personalcare.manualsonline.com/manuals/device/light_therapy_device.html","http://personalcare.manualsonline.com/manuals/device/medical_alarms.html","http://personalcare.manualsonline.com/manuals/device/microscope_and_magnifier.html","http://personalcare.manualsonline.com/manuals/device/home_care_product.html","http://personalcare.manualsonline.com/manuals/device/hair_dryer.html","http://personalcare.manualsonline.com/manuals/device/hair_dryer.html","http://personalcare.manualsonline.com/manuals/device/hearing_aid.html","http://personalcare.manualsonline.com/manuals/device/hair_clippers.html","http://personalcare.manualsonline.com/manuals/device/electric_shaver.html","http://personalcare.manualsonline.com/manuals/device/electric_toothbrush.htmlh","ttp://personalcare.manualsonline.com/manuals/device/hair_care_product.html","http://personalcare.manualsonline.com/manuals/device/electric_shaver.html" , "http://personalcare.manualsonline.com/manuals/device/blood_pressure_monitor.html", "http://personalcare.manualsonline.com/manuals/device/mobility_aid.html","http://personalcare.manualsonline.com/manuals/device/scale.html","http://personalcare.manualsonline.com/manuals/device/thermometer.html"]
    # allowed_domains = ["personalcare.manualsonline.com", "manualsonline.com"]
    #start_urls_Kitchen = ["http://kitchen.manualsonline.com/manuals/mfg/kenmore/kenmore_product_list.html", "http://kitchen.manualsonline.com/manuals/mfg/hotpoint/hotpoint_product_list.html", "http://kitchen.manualsonline.com/manuals/mfg/fisher_paykel/fisher_paykel_product_list.html", "http://kitchen.manualsonline.com/manuals/device/dishwasher.html","http://kitchen.manualsonline.com/manuals/device/refrigerator.html","http://kitchen.manualsonline.com/manuals/device/microwave_oven.html", "http://kitchen.manualsonline.com/manuals/device/bread_maker.html", "http://kitchen.manualsonline.com/manuals/device/can_opener.html", "http://kitchen.manualsonline.com/manuals/device/coffee_grinder.html", "http://kitchen.manualsonline.com/manuals/device/coffeemaker.html", "http://kitchen.manualsonline.com/manuals/device/convection_oven.html", "http://kitchen.manualsonline.com/manuals/device/cooktop.html", "http://kitchen.manualsonline.com/manuals/device/cookware.html", "http://kitchen.manualsonline.com/manuals/device/dishwasher.html", "http://kitchen.manualsonline.com/manuals/device/double_oven.html", "http://kitchen.manualsonline.com/manuals/device/egg_cooker.html", "http://kitchen.manualsonline.com/manuals/device/electric_cookie_press.html", "http://kitchen.manualsonline.com/manuals/device/electric_garlic_roaster.html", "http://kitchen.manualsonline.com/manuals/device/electric_pressure_cooker.html", "http://kitchen.manualsonline.com/manuals/device/electric_steamer.html", #"http://kitchen.manualsonline.com/manuals/device/espresso_maker.html", "http://kitchen.manualsonline.com/manuals/device/fondue_maker.html", "http://kitchen.manualsonline.com/manuals/device/food_processor.html", "http://kitchen.manualsonline.com/manuals/device/food_saver.html", "http://kitchen.manualsonline.com/manuals/device/food_warmer.html", "http://kitchen.manualsonline.com/manuals/device/freezer.html", "http://kitchen.manualsonline.com/manuals/device/frozen_dessert_maker.html", "http://kitchen.manualsonline.com/manuals/device/fryer.html", "http://kitchen.manualsonline.com/manuals/device/garbage_disposal.html" ,"http://kitchen.manualsonline.com/manuals/device/hot_beverage_maker.html" ,"http://kitchen.manualsonline.com/manuals/device/hot_beverage_maker.html" ,"http://kitchen.manualsonline.com/manuals/device/ice_maker.html" ,"http://kitchen.manualsonline.com/manuals/device/ice_tea_maker.html" ,"http://kitchen.manualsonline.com/manuals/device/juicer.html" ,"http://kitchen.manualsonline.com/manuals/device/kitchen_entertainment_center.html" , "http://kitchen.manualsonline.com/manuals/device/kitchen_grill.html" , "http://kitchen.manualsonline.com/manuals/device/griddle.html" ,"http://kitchen.manualsonline.com/manuals/device/kitchen_utensil.html" ,"http://kitchen.manualsonline.com/manuals/device/meat_grinder.html", #"http://kitchen.manualsonline.com/manuals/device/microwave_oven.html" ,"http://kitchen.manualsonline.com/manuals/device/mixer.html" ,"http://kitchen.manualsonline.com/manuals/device/oven.html" ,"http://kitchen.manualsonline.com/manuals/device/oven_accessories.html" ,"http://kitchen.manualsonline.com/manuals/device/pasta_maker.html" ,"http://kitchen.manualsonline.com/manuals/device/corn_popper.html" ,"http://kitchen.manualsonline.com/manuals/device/quesadilla_maker.html" ,"http://kitchen.manualsonline.com/manuals/device/range.html" ,"http://kitchen.manualsonline.com/manuals/device/refrigerator.html" ,"http://kitchen.manualsonline.com/manuals/device/rice_cooker.html" ,"http://kitchen.manualsonline.com/manuals/device/slow_cooker.html" ,"http://kitchen.manualsonline.com/manuals/device/toaster.html" ,"http://kitchen.manualsonline.com/manuals/device/tortilla_maker.html" ,"http://kitchen.manualsonline.com/manuals/device/trash_compactor.html" ,"http://kitchen.manualsonline.com/manuals/device/trash_compactor.html", "http://kitchen.manualsonline.com/manuals/device/ventilation_hood.html", "http://kitchen.manualsonline.com/manuals/device/waffle_iron.html", "http://kitchen.manualsonline.com/manuals/device/water_dispenser.html", "http://kitchen.manualsonline.com/manuals/device/wok.html", "http://kitchen.manualsonline.com/manuals/device/yogurt_maker.html"]

    def check_if_file_already_is_pdf(self, category):
        for pdf in pdf_names:
            try:
                if self.cur_m[0:len(self.cur_m) - 3] == pdf[0:len(self.cur_m)-3]:
                    rename_pdf(pdf, category)
            except:
                continue

    def rename_pdf(self, pdf_path, category):
        os.rename(CUR_PDF_PATH + pdf_path , CUR_PDF_PATH + category + pdf_path)


    def parse(self, response):
        self.logger.info(response.request.url)
        self.cur_m = (response.request.url.split('/')[-2] +'_' + response.request.url.split('/')[-1]).split('.')[0]
        print(self.cur_m)
        for href in response.css('a[href$=".pdf"]::attr(href)').extract():
            self.logger.info("in parse article loop")

            yield response.follow(href, callback=self.save_pdf)

        for href in response.css('h5 a::attr(href)'):
            yield response.follow(href, callback=self.parse)

    # def parse_article(self, response):
    #     self.logger.info("entered parse article")
    #     for href in response.css('a[href$=".pdf"]::attr(href)').extract():
    #         self.logger.info("in parse article loop")
    #         yield response.follow(href, callback=self.save_pdf)

    def save_pdf(self, response):
        self.logger.info(self.cur_m)
        self.logger.info('Saving PDF %s', self.cur_m)
        with open(self.cur_m + ".pdf", 'wb') as f:
            f.write(response.body)


def get_all_file_names():
    return os.listdir(CUR_PDF_PATH)

if __name__ == '__main__':
    from scrapy import cmdline
    pdf_names = get_all_file_names()

    cmdline.execute("scrapy crawl pdf".split())
