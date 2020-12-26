# prerequisites
# install selenium web driver using pip
from selenium import webdriver
import time
import random
from passwords import password

errors = 0
over_500_list = []
# initialize selenium webdriver
driver = webdriver.Chrome()
# driver.get("https://google.com")
driver.get("https://www.instagram.com/")

# sleep for 2 seconds to let instagram load
time.sleep(2)

def login(user, passwd):
    # get username element and input value to it
    username_inp = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    username_inp.send_keys(user)

    # get password element and input value to it
    password_inp = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    password_inp.send_keys(passwd)

    # click login button
    login_button = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
    login_button.click()

    # let the page load for another 2 seconds
    time.sleep(4)

    # # click not now button
    # not_now_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button')
    # not_now_button.click()
    #
    # time.sleep(4)
    # # decline notifications
    # decline_notification_button = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
    # decline_notification_button.click()


def get_users(user_url):
    # go to account url
    driver.get(user_url)

    # random time interval after going to the account page
    a = random.random()
    b = random.randint(2, 3)
    time.sleep(a + b)
    # get follower count
    follower_count = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title')
    follower_count = int(follower_count.replace(',',''))
    print('Follower Count:', follower_count)

    # click on followers button
    followers = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
    followers.click()
    # random time interval after clicking on follower button
    a = random.random()
    b = random.randint(2, 4)
    time.sleep(a+b)

    user_list = []
    global errors
    count = 1
    for i in range(12, (follower_count+13), 12):
        # scroll down to load all folower elements
        try:
            # will get an error without this since its not going to find an element with list number over follower count
            user = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li[' + str(i) + ']')
            driver.execute_script("arguments[0].scrollIntoView();", user)
            a = random.random()
            b = random.randint(2,4)
            time.sleep(a+b)
        except:
            # if there is an error this means we're at the last few followers and just keep continuing the loop without scrolling
            pass

        for x in range(count, (i)):
            try:
                # get all the user links from the previous i value to the next i value
                user = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li[' + str(x) + ']/div/div[1]/div[2]/div[1]/span/a')\
                    .get_attribute("href")          #/html/body/div[5]/div/div/div[2]/ul/div/li[25]/div/div[1]/div[2]/div[1]/span/a
                user_list.append(user)              #/html/body/div[5]/div/div/div[2]/ul/div/li[73]/div/div[1]/div[2]/div[1]/span/a
                print(user)                         #/html/body/div[5]/div/div/div[2]/ul/div/li[73]/div/div[1]/div[2]/div[1]/span/a
                if x == follower_count:
                    print('Followers Scraped:',len(user_list))
                    print('Errors:', errors)
                    # stop the loop when the last follower is done
                    break
            except:
                print('Follower Error')
                errors += 1

        count = i

    print('Errors:', errors)
    print('User List:', user_list)
    print('Number of Follower Links Obtained:', len(user_list))
    return user_list

def write_to_file(users):
    # open file
    filename = "user_list.csv"
    f = open(filename, "w")

    # set headers
    headers = "Links\n"
    f.write(headers)

    for i in users:
        # write results to file
        f.write('=HYPERLINK("' + i + '")' + '\n')


def check_users(users):
    accounts_over_500 = []
    public_list = []
    private_list = []
    # check if accounts are public or private
    for i in users:
        print(i)
        # open the user account page
        driver.get(i)
        a = random.random()
        b = random.randint(2, 3)
        time.sleep(a+b)
        # get follower count
        follower_count = 0
        try:
            # finding follower element for private accounts
            follower_count = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/span/span').get_attribute('title')
        except:
            try:
                # finding follower element for public accounts
                follower_count = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title')

            except:
                print('Follower Count Not Found')
                continue

        # print('Follower Count:', follower_count)
            # remove commas from follower counts more than 1000

        follower_count = follower_count.replace(',','')
        if int(follower_count) >= 500:
            accounts_over_500.append(i)
            print('Account has more than 500 Folowers')
        # find the private text
        text = ''
        try:
            text = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div/div/h2').text
        except:
            try:
                text = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[2]/article/div/div/h2').text
            except:
                try:
                    text =  driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div[1]/div/h2').text

                except:
                    print('Account Not Private')
                    public_list.append(i)

        if 'Private' in text:
            print('Account Private')
            private_list.append(i)

    print('Public Accounts:', public_list)
    print('Number of Public Accounts:', len(public_list))
    print(accounts_over_500)
    print('Accounts with over 500 followers:', len(accounts_over_500))
    return public_list, accounts_over_500


def process_generation(public_list):
    global over_500_list
    new_public_list = []
    for i in public_list:
        print('looping for:', i)
        user_list = get_users(i)
        temp_public_list, new_accounts_over_500 = check_users(user_list)
        new_public_list.append(temp_public_list)
        over_500_list.append(new_accounts_over_500)
        print('public list for this account:', temp_public_list)
        print('accounts_over_500 for this account:', new_accounts_over_500)
    print('final over 500 so far:', over_500_list)
    print('public list for this generation:', new_public_list)
    return new_public_list



#user_list = ['https://www.instagram.com/_its.asindu/', 'https://www.instagram.com/_raayan._/', 'https://www.instagram.com/siluni.17/', 'https://www.instagram.com/itstaco07/', 'https://www.instagram.com/ruwi.ya/', 'https://www.instagram.com/deha.nsi/', 'https://www.instagram.com/avi_sh_ka__/', 'https://www.instagram.com/pererasathnara/', 'https://www.instagram.com/janith_0904/', 'https://www.instagram.com/dakshina_perera/', 'https://www.instagram.com/iam_rk17/', 'https://www.instagram.com/hirudika1154/', 'https://www.instagram.com/eungalean/', 'https://www.instagram.com/lazylemon__/', 'https://www.instagram.com/_.nulan._/', 'https://www.instagram.com/aiyoo.usman/', 'https://www.instagram.com/ayami.w_/', 'https://www.instagram.com/minz.14/', 'https://www.instagram.com/hideawaytrails_by_chaarya/', 'https://www.instagram.com/filip_fernando/', 'https://www.instagram.com/shanindu_pushkara/', 'https://www.instagram.com/_yesh_xvi_/', 'https://www.instagram.com/anjanathemi/', 'https://www.instagram.com/asiiiiii___/', 'https://www.instagram.com/jayithmn_17/', 'https://www.instagram.com/offofreddit/', 'https://www.instagram.com/tanish.rangnekar/', 'https://www.instagram.com/cyberwolf420/']
#public_list = ['https://www.instagram.com/_its.asindu/', 'https://www.instagram.com/iam_rk17/', 'https://www.instagram.com/hirudika1154/', 'https://www.instagram.com/eungalean/', 'https://www.instagram.com/_.nulan._/', 'https://www.instagram.com/aiyoo.usman/', 'https://www.instagram.com/hideawaytrails_by_chaarya/', 'https://www.instagram.com/anjanathemi/', 'https://www.instagram.com/offofreddit/', 'https://www.instagram.com/cyberwolf420/', 'https://www.instagram.com/sathutulanka/', 'https://www.instagram.com/umeshagmail.commadush/', 'https://www.instagram.com/sasmithaa_h.g/', 'https://www.instagram.com/dinuwabro/', 'https://www.instagram.com/aliya.rinaldi/', 'https://www.instagram.com/the_viper_hizzess/', 'https://www.instagram.com/ilbkgloballtd/', 'https://www.instagram.com/hammvdh/', 'https://www.instagram.com/__abhi.___.shek__/', 'https://www.instagram.com/proudgaming_/', 'https://www.instagram.com/shen.shen15/', 'https://www.instagram.com/lyceum_info_experts/', 'https://www.instagram.com/thidasaponsu/', 'https://www.instagram.com/wklakshan/', 'https://www.instagram.com/theprincess2745/', 'https://www.instagram.com/thoufeek.thoufeek.35175/', 'https://www.instagram.com/presshandstands5772018/', 'https://www.instagram.com/dini_.th/', 'https://www.instagram.com/sandive_d/', 'https://www.instagram.com/slayingqueen.xv/', 'https://www.instagram.com/deshan_jayasinghe/', 'https://www.instagram.com/naviya1996/', 'https://www.instagram.com/scandlegrimes/', 'https://www.instagram.com/luthira75/', 'https://www.instagram.com/mr_buha_/', 'https://www.instagram.com/sandusamanali/', 'https://www.instagram.com/tharushadeegay/', 'https://www.instagram.com/nanmyoved/', 'https://www.instagram.com/____playboi/', 'https://www.instagram.com/death_kid_mineth/', 'https://www.instagram.com/harder_than_ever5566/', 'https://www.instagram.com/_lakzzndu_/', 'https://www.instagram.com/_.mahesh.silva._/', 'https://www.instagram.com/__gayaa___/', 'https://www.instagram.com/kavideed/', 'https://www.instagram.com/_.thevirillex._/', 'https://www.instagram.com/kehanperera/', 'https://www.instagram.com/kiaraaashelani_/', 'https://www.instagram.com/akeelrox/', 'https://www.instagram.com/___.sammy__/', 'https://www.instagram.com/cc.vxz/', 'https://www.instagram.com/canada__bro0303/', 'https://www.instagram.com/death_vader_12/', 'https://www.instagram.com/its_me_zama/', 'https://www.instagram.com/sucker_4_pain7059/', 'https://www.instagram.com/angelicapatel3584/', 'https://www.instagram.com/henna.by.h_u_z_z_/', 'https://www.instagram.com/iamaguyunknown123/', 'https://www.instagram.com/senanayakegevindu/', 'https://www.instagram.com/s_a_v_v_a_/', 'https://www.instagram.com/crz__fauza/', 'https://www.instagram.com/whalee.12/', 'https://www.instagram.com/rashenwanniarachchibro/', 'https://www.instagram.com/rashen_bro/', 'https://www.instagram.com/divuper23/', 'https://www.instagram.com/aakifnaushad/', 'https://www.instagram.com/steve_border_123/', 'https://www.instagram.com/roxjay25/', 'https://www.instagram.com/rimas_yah_0001/', 'https://www.instagram.com/bdhfnfbdjsmdh/', 'https://www.instagram.com/areeb_thug/', 'https://www.instagram.com/ramidapeiris/', 'https://www.instagram.com/luthirainstargram9498/', 'https://www.instagram.com/ethelr.finch/', 'https://www.instagram.com/rachelryrie/', 'https://www.instagram.com/ruwa9153/', 'https://www.instagram.com/g_e_n_t_e_l_m_e_n/', 'https://www.instagram.com/indikajayasinghe18/', 'https://www.instagram.com/pissu_kaviya/', 'https://www.instagram.com/___failiure___/', 'https://www.instagram.com/veenaviamanda/', 'https://www.instagram.com/ushan_00715/', 'https://www.instagram.com/dammikapriyani/', 'https://www.instagram.com/jameswalker2326/', 'https://www.instagram.com/raneshranesh/', 'https://www.instagram.com/_su.rvi.vor_/', 'https://www.instagram.com/sheww_shez/', 'https://www.instagram.com/karaceitlyn/', 'https://www.instagram.com/a.benedict_john/', 'https://www.instagram.com/banu.jay/', 'https://www.instagram.com/luthira_/', 'https://www.instagram.com/janakasudusinghe/', 'https://www.instagram.com/fk_lyf_i_luv_u/', 'https://www.instagram.com/coolguy7502/', 'https://www.instagram.com/cj_zack_stones/', 'https://www.instagram.com/gevindusenanayake/', 'https://www.instagram.com/cristian_s701/', 'https://www.instagram.com/raviruhan6643/', 'https://www.instagram.com/mathildelasardine/', 'https://www.instagram.com/shahrbunoo_ramezani/', 'https://www.instagram.com/meowmeowpusane/', 'https://www.instagram.com/cristian_sanchez_701/', 'https://www.instagram.com/rednity/', 'https://www.instagram.com/tomatenmarx/', 'https://www.instagram.com/i_procrastinate_alot/', 'https://www.instagram.com/fm_fizzy/']


# define user name(password is defined in seperate file)
username = 'drksmth21'
# login
login(username, password) #call login function
# go to a specific public profile and get follower list
user_list = get_users('https://www.instagram.com/drake_smth/')
# get the public list and the accounts over 500 using the new follower list
public_list, accounts_over_500 = check_users(user_list)
print(public_list)
print(accounts_over_500)
# get the next generation of public accounts and add the current gen's accounts over 500 followers accordingly
new_public_list = process_generation(public_list)
print('new public list:', new_public_list)

# write to file a list of user links
    # write_to_file(user_list)