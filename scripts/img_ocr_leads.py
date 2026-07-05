import json, re

# OCR transcriptions from the 5 photos (name, phone_raw, extra, country)
img1 = """5441.23364|Banan Zain Hasan Al Sharif Al Zaabi|43688
5611294111|Rugaya Abdulla Ibrahim Al Ali|43888
5021821166|Ibrahim Mohammed Noor Ahmad Abdulla Bi|43788
339100007|Feryal Khaled Ayed Fahad|43688
723901222|Hassan Ali Khalife|79288
507142723|Fawzia Ali Yousuf Ahmed Al Ali|43888
5001528552|Khalid Saud M Al Bishir|74088
5223229.29|Hend Humaid Abdulla Alshaiba Alnuaimi|44088
5089058888|Ahmed Sulaiman Khalfan Ali Alhassani|43688
502236080|Fatima Sulaiman Khalfan Ali Alhassani|43688
5699355559|Haya Mohammed A Almunif|43988
818260111|Muntadhar Kathem Khalaf|45088
5556674.9|Shiekha Najla Saoud J M Al-Thani|44888
5926111114|Duha Omar Darwich|
71025288|Zahraa Khalifeh|
699119572222|Peter Pavlovic|46488
509982948|Ali Mubarak Abdulla Mohamed Alhammadi|78088
2146376924|Haneen Issa Lazim Almaarfawi|79088
6492238231|Linda R Jasin|45988
567646499.7|Abdulaziz Hamoud A Albarrak|74088
178226130414|Firas Mayouf Altahhan|
770517022|Muhanned Karim Ali Ali|79488
6604250646|Gerhard Froschl|75088
1005740057|Omar Mostafa Ahmed El Serafy|84188
661660724|Said Iboukhoulef|
5668207.4|Syed Mohammad Intezar Mehdi|45388
655926162 / 568201376|Mounia Benidir|84488
738929034.5|Said Hazim Reshak Al Haidari|74288
555386469|Amira Adel Mohamed Eladl|
5038051979|Eisar Asim Abdalla Alkhalifa|"""

img2 = """S0313S522|Suaad Ahmed Saad Mohammed Bakari|
5444/348|Shamsa Khalfan Mubarak Saleem Alyagoub|
50622295|Mariam Matar Obaid|
S0622918S|Amer Salem Ahmed Janaan Alseiari|
550153311|Hallo Ghalb Obeed Al-Kaki|
S2121245|Asmaa Abdul Jabbar Ismeeel|
S5592068|Suliyman Shifa Ahmed|
S 8832678|Anood Hamza Hasan Salem Alsuwaidi|
9 9 S5533|Yazeed Mohamed Saud Al Sulaimi|
770466295|Ahmed Said Chikh|
7401129096|Selvana Salim Sadeq Doda|
7507532152|Dajel Sabeeh Shamoon Al-Qes Hanna|
968324424|Firas Souhel Badi|
S06331317|Krishan Kumar Tarachand|
S5036657|Reyad Djennadi|
S423332S39|Abeer Omar Khalil|
S5800220|Amina Mohammad Sharif Rahimi Halri|
4312091|Toufik Benallouch|
823808662|Avinash Rooplall Harpal|
S0166500|Ahlam Nasser Khamis Nasser Alalawi|
S539090|Khalid Obaid Khamis Obaid Al Muhairi|
S0454254S|Maitha Ahmad Murad Mohamad Aljamri|
4848478|Omar Nems|
6034020|Ejike Azubuike Mojekwu|
90834921|Anthony Chinweuba Okoro|
S61846|Chukwudi Emmanuel Obinwa|
S06251|Maryam Ghuloom Abbas|
S0286656|Sharifa Abdulla Abdulla Mohammad Alhaj"""

img3 = """9246490602|Aleksel Briankin|44888
9728250205|Valerii Golovko|44888
9184208464|Larisa Chernlaeva|44988
9128047|Yasir Osman Hamed Ahmed|73888
9128554267|Bella Rodina|44888
9251146230|Galina Anopka|46088
9852466488|Liaisan Razapova|44888
9082209200|Sirvan Ebrahim Mohammadian|
9632487624|Andrei Iurev|44888
9149055505|Aleksei Ambrosov|
9162260520|Elena Sharova|84688
9091533226|Irina Dolbilina|81688
5886421149|Myrat Myradov|77288
9124520060|Anna Bolotova|75888
5570409869|Hadar Mokhtar Abdullah Al Sakkaf|75988
9282604344|Anzhelika Novoselova|
5035279275|Samson Mathews George George Mathew|
9049360550|Magomedsaid Gasanov|
9254427497|Natalia Pianko|
7645075|Berfin Altun|
9999815000|Nadeem Malik|
9688589212|Irina Mankova|
7645293402|Britta Conrad|
7286216410|Ayub Yusuf Shaikh|
9274210236|Azat Abusev|
5685172260|Tatiana Ufimtceva|
9283196666|Zaur Kardanov|
9263006666|Arsen Sosmakov|
5666928225|Ali khan Marjan Gul|
1416301161|Abdelwahab A Arrazaghi|"""

img4 = """5692151123|Mohamed Althaf Mohamed Naseem|
5917800008|Zaif Ullah Muhammad Riaz|
559147939|Fatima Chaari|7820
5392216613|Mohamad Helal Saleh Maratia|
40769020|Oras Saleh Mehdi|
50816346|Saqib Marfani Zubair Marfani|
9442401515|Agop Malkoun Malkon|7980
526709996|Amr Mahmdouh Mohamed Ahmed|7438
915521733|Alexander Zhilnikov|8008
9622159907|Seid Shakhbanov|
5080l3991|Adil Bashri Osman Elhaj|
919132b317|Oxana Serikova|7528
51151242|Abdulsalam Mhd Said Alsioufi|
50196559|Khadidja Drici|
561371942|Ibrahim Ahmed El Badawi Abdelsatar|
3931043083|Diletta Guarino|7868
5080988973|Mohammad Mostafa Farz|
77200061|Sfin Kareem Fadhil|
501415080|Shaikh Salem Faisal Sultan Salem Alqasimi|
561289223|Rizwan Moazzam Siddiqui Moazzam Uddin S|
562832047|Lata Ganisetty Venkat Rao Ganisetty|
9301492222|Andrey Kanashin|7748
9255116330|Galina Anooka|9208
9852263111|Oleg Kulikov|
9128182283|Malek Malual Diing Deng|
9121059117|Mohamed Abdalla Mohieldin Gaily|
4471818929|Vladislav Geiko|6719
561285331|Denis Makhnev|
415878909|Vladislav Geiko|6732
542261699|Mohammad Aziz Mohammadian|
1280951b1|Ataallah Ali Mahmoudi|
5688094541|Mohammad Ebrahim Mohammadian|"""

# img5: country|phone|name
img5 = """|55591605|Viktoria Ugrozova
|918522352|Aleksandr Kovshun
|9153056026|Anna Bondarenko
|9217750015|Ivan Savenchuk
|709382301|Mohammed Faisal Ghazi Al-Siaghy
|56399505 5|Hashim Issa Timan Abdalrahman
|9026156544|Olesia Nikolaeva
|916840360|Taha Bartug Kanik
|9141208709 5|Dizaar Hussein Abdalla Abdalla
|720987532|Saman Ahmad Rasouli
|7231247004|Lothar Weinz
|9122172679|Ardak Kalmagambetov
|9130414222|Andrey Kanashin
|615522631|Ziad Al Zuhairi
australia|4128725873|Wisam Lahd
paraguay|488545969|Nilgun Hisar
spain|2928445823|Ghazanfar Bashir
uae|9029954017|Garik Gapoian
uae|9645501 46|Zhanna Nurakhmetova
egypt|927741392|Elena Kniazeva
events|4166204|Stefan Iric
germany|1772575999|Eckhardt Klinksiek
|50460962|Najeeb Abdul Gaffoor Peeru kannu Abdul
uae|9046103236|Mikhail Voytovich
|5932740980|Diego Isaac Benitez Canete
japan|702947084|Alexey Turchenko
|5618647|Mohammed Abbas S Al Zain
|788261620|Ayub Yusuf Shaikh
||Aziz Anvarovich Maraimov
||Krystsina Nebytava
||Jaroslav Grigorev
||Tahseen Jasim Hussein Husseen"""

srcmap={'img1':'0f446bd0-8e73-46bd-a82a-03fc5232fa28.jpg',
        'img2':'3733d235-0d95-46e1-a62d-597cc5ca6ed6.jpg',
        'img3':'3bfe2974-f503-4bb0-9bd3-dc2ba7597f20.jpg',
        'img4':'8380efe1-9609-4e66-a228-fe4b9750f5ce.jpg',
        'img5':'bfd53b94-ddbf-411b-be01-a4bae9670d96.jpg'}

def clean_phone(p):
    if not p: return '',[]
    raw=p.strip()
    # split multi
    parts=re.split(r'[\/]', raw)
    nums=[]
    for pt in parts:
        d=re.sub(r'\D','',pt)
        if len(d)>=6: nums.append(d)
    return raw, nums

leads=[]
def add(block, key, country_first=False):
    for line in block.strip().split('\n'):
        cols=line.split('|')
        if country_first:
            country=cols[0].strip(); phone=cols[1].strip() if len(cols)>1 else ''; name=cols[2].strip() if len(cols)>2 else ''
            extra=''
        else:
            phone=cols[0].strip(); name=cols[1].strip() if len(cols)>1 else ''; extra=cols[2].strip() if len(cols)>2 else ''
            country=''
        raw,nums=clean_phone(phone)
        leads.append({'name':name,'phone_raw':raw,'phones':nums,'extra':extra,
                      'country':country,'source_image':srcmap[key],'origin':'photo-OCR'})

add(img1,'img1'); add(img2,'img2'); add(img3,'img3'); add(img4,'img4')
add(img5,'img5',country_first=True)

IMG_LEADS = leads   # exported for build.py

if __name__ == "__main__":
    print('image leads:',len(leads))
    print('with phone digits:',sum(1 for l in leads if l['phones']))
    for l in leads[:3]: print(l)
