from spider.models import crawlerModel

entry = crawlerModel(test_key='arthur')
entry.test_value = 'Wang'
entry.save()



for entry in crawlerModel.objects:
    print entry.test_key