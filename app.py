import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="健康餐助手（蛋白优化版）", layout="centered")
st.title("🥗 健康餐助手 — 蛋白优化版（午晚蛋白不重复）")

# ---------------- 用户输入 ----------------
height = st.number_input("身高 (cm)", 100, 250, 170)
weight = st.number_input("体重 (kg)", 30, 200, 65)
age = st.number_input("年龄", 10, 100, 25)
gender = st.selectbox("性别", ["男", "女"])
goal = st.selectbox("目标", ["减脂", "保持", "增肌"])

# ---------------- 计算每日目标 ----------------
bmr = 10*weight + 6.25*height - 5*age + (5 if gender=="男" else -161)
factor = 1.2 if goal=="减脂" else 1.4 if goal=="保持" else 1.6
sex_adj = 1.05 if gender=="男" else 0.95
calories_per_day = int(bmr * factor * sex_adj)
protein_g = int(weight * (1.8 if gender=="男" else 1.6))
fat_g = int(calories_per_day*0.25/9)
carb_g = int(calories_per_day*0.5/4)

protein_dist = {"早餐":0.25,"午餐":0.3,"晚餐":0.3,"加餐":0.15}

st.markdown(f"**每日目标**：热量 {calories_per_day} kcal ｜ 蛋白质 {protein_g} g ｜ 碳水 ≈ {carb_g} g ｜ 脂肪 ≈ {fat_g} g")

# ---------------- 食物库 ----------------
food_db = {
    # 蛋白质
    "鸡胸肉":{"cal":165,"p":31,"c":0,"f":3.6,"type":"protein"},
    "牛肉":{"cal":250,"p":26,"c":0,"f":15,"type":"protein"},
    "三文鱼":{"cal":208,"p":20,"c":0,"f":13,"type":"protein"},
    "鸡蛋":{"cal":155,"p":13,"c":1,"f":11,"type":"protein"},
    "鸭胸肉":{"cal":195,"p":23,"c":0,"f":7,"type":"protein"},
    "火鸡胸肉":{"cal":135,"p":30,"c":0,"f":1,"type":"protein"},
    "虾仁":{"cal":85,"p":20,"c":0,"f":1.2,"type":"protein"},
    "鳕鱼":{"cal":105,"p":23,"c":0,"f":1,"type":"protein"},
    "蛋白棒":{"cal":120,"p":20,"c":10,"f":2,"type":"protein"},
    "酸奶":{"cal":59,"p":10,"c":3.6,"f":0.4,"type":"protein"},
    "低脂牛奶":{"cal":42,"p":3.4,"c":5,"f":1,"type":"protein"},

    # 碳水
    "燕麦片":{"cal":389,"p":17,"c":66,"f":7,"type":"carb"},
    "糙米":{"cal":111,"p":2.6,"c":23,"f":0.9,"type":"carb"},
    "红薯":{"cal":86,"p":1.6,"c":20,"f":0.1,"type":"carb"},
    "全麦面包":{"cal":247,"p":13,"c":41,"f":4.2,"type":"carb"},
    "藜麦":{"cal":120,"p":4,"c":21,"f":1.9,"type":"carb"},
    "土豆":{"cal":77,"p":2,"c":17,"f":0.1,"type":"carb"},

    # 蔬菜
    "西兰花":{"cal":55,"p":3.7,"c":11,"f":0.6,"type":"veg"},
    "菠菜":{"cal":23,"p":2.9,"c":3.6,"f":0.4,"type":"veg"},
    "四季豆":{"cal":31,"p":1.8,"c":7,"f":0.1,"type":"veg"},
    "芦笋":{"cal":20,"p":2.2,"c":3.9,"f":0.1,"type":"veg"},
    "蘑菇":{"cal":22,"p":3.1,"c":3.3,"f":0.3,"type":"veg"},
    "胡萝卜":{"cal":41,"p":0.9,"c":10,"f":0.2,"type":"veg"},
    "青椒":{"cal":20,"p":1,"c":4.5,"f":0.2,"type":"veg"},
    "黄瓜":{"cal":16,"p":0.7,"c":3.6,"f":0.1,"type":"veg"},
    "番茄":{"cal":18,"p":0.9,"c":3.9,"f":0.2,"type":"veg"},

    # 水果
    "苹果":{"cal":52,"p":0.3,"c":14,"f":0.2,"type":"fruit"},
    "香蕉":{"cal":89,"p":1.1,"c":23,"f":0.3,"type":"fruit"},
    "橙子":{"cal":47,"p":0.9,"c":12,"f":0.1,"type":"fruit"},
    "蓝莓":{"cal":57,"p":0.7,"c":14,"f":0.3,"type":"fruit"},
    "草莓":{"cal":33,"p":0.7,"c":8,"f":0.3,"type":"fruit"},
    "猕猴桃":{"cal":61,"p":1.1,"c":15,"f":0.5,"type":"fruit"},

    # 脂肪
    "坚果":{"cal":607,"p":20,"c":21,"f":54,"type":"fat"},
    "牛油果":{"cal":160,"p":2,"c":9,"f":15,"type":"fat"},
}

# ---------------- 核心函数 ----------------
def grams_for_protein(food_key, target_p):
    info = food_db.get(food_key)
    if not info: return 50
    return max(50,int(target_p*100/info["p"]))

def allocate_meal(meal_template, protein_target, cal_target, allow_protein2=True):
    items=[]
    prot_keys=[meal_template.get("protein")]
    if allow_protein2 and meal_template.get("protein2"):
        prot_keys.append(meal_template.get("protein2"))

    per_prot_target = protein_target / len(prot_keys) if prot_keys else 0
    for k in prot_keys:
        info = food_db.get(k)
        if not info: continue
        g = grams_for_protein(k, per_prot_target)
        # 保证 protein ≥ protein2 2倍
        if len(prot_keys) == 2 and k == prot_keys[0]:
            g = max(g, grams_for_protein(prot_keys[1], per_prot_target)*2)
        cal=int(info["cal"]*g/100)
        p=int(info["p"]*g/100)
        c=int(info["c"]*g/100)
        f=int(info["f"]*g/100)
        items.append((k,g,cal,p,c,f))

    for role in ["carb","veg","fruit","fat"]:
        k = meal_template.get(role)
        if k:
            info = food_db.get(k)
            if not info or info["type"]!=role: continue
            g=100
            cal=int(info["cal"]*g/100)
            p=int(info["p"]*g/100)
            c=int(info["c"]*g/100)
            f=int(info["f"]*g/100)
            items.append((k,g,cal,p,c,f))

    total_cal=sum(it[2] for it in items)
    if total_cal>0:
        adjust_ratio=cal_target/total_cal
        new_items=[]
        for name,g,cal,p,c,f in items:
            info = food_db.get(name)
            new_g=int(g*adjust_ratio)
            new_items.append((name,new_g,int(info["cal"]*new_g/100),
                              int(info["p"]*new_g/100),int(info["c"]*new_g/100),int(info["f"]*new_g/100)))
        items=new_items

    sum_cal=sum(it[2] for it in items)
    sum_p=sum(it[3] for it in items)
    sum_c=sum(it[4] for it in items)
    sum_f=sum(it[5] for it in items)
    return items, int(sum_cal), int(sum_p), int(sum_c), int(sum_f)

# ---------------- 早中晚加餐模板 ----------------
def shuffle_pool(pool):
    tmp = pool[:]
    random.shuffle(tmp)
    return tmp

breakfast_pool = shuffle_pool([
    {"protein":"鸡蛋","carb":"燕麦片","fruit":"香蕉"},
    {"protein":"酸奶","carb":"燕麦片","fruit":"蓝莓"},
    {"protein":"鸡蛋","carb":"全麦面包","fruit":"苹果"},
    {"protein":"低脂牛奶","carb":"燕麦片","fruit":"猕猴桃"},
    {"protein":"酸奶","carb":"全麦面包","fruit":"草莓"},
    {"protein":"鸡蛋","carb":"藜麦","fruit":"蓝莓"},
    {"protein":"低脂牛奶","carb":"全麦面包","fruit":"橙子"},
])

snack_pool = shuffle_pool([
    {"protein":"酸奶","fruit":"蓝莓"},
    {"protein":"苹果","fat":"坚果"},
    {"protein":"坚果","fruit":"香蕉"},
    {"protein":"酸奶","fruit":"猕猴桃"},
    {"protein":"香蕉","fat":"牛油果"},
    {"protein":"低脂牛奶","fruit":"草莓"},
])

lunch_pool = shuffle_pool([
    {"protein":"鸡胸肉","carb":"糙米","veg":"西兰花"},
    {"protein":"三文鱼","carb":"糙米","veg":"菠菜"},
    {"protein":"牛肉","carb":"红薯","veg":"四季豆"},
    {"protein":"鸭胸肉","carb":"糙米","veg":"蘑菇"},
    {"protein":"鸡胸肉","carb":"全麦面包","veg":"菠菜"},
    {"protein":"鳕鱼","carb":"藜麦","veg":"西兰花"},
    {"protein":"火鸡胸肉","carb":"红薯","veg":"芦笋"},
])

dinner_pool = shuffle_pool([
    {"protein":"鸡胸肉","carb":"糙米","veg":"芦笋"},
    {"protein":"三文鱼","carb":"红薯","veg":"西兰花"},
    {"protein":"牛肉","carb":"土豆","veg":"菠菜"},
    {"protein":"火鸡胸肉","carb":"土豆","veg":"蘑菇"},
    {"protein":"虾仁","carb":"全麦面包","veg":"青椒"},
    {"protein":"鳕鱼","carb":"藜麦","veg":"菠菜"},
    {"protein":"鸭胸肉","carb":"糙米","veg":"西兰花"},
])

# ---------------- 一周菜单生成 ----------------
def generate_week_menu(bf_pool,l_pool,d_pool,s_pool,protein_g,calories_per_day):
    week=[]
    protein2_options = ["豆腐","虾仁","鳕鱼","牛肉"]
    random.shuffle(protein2_options)
    protein2_used = []

    for i in range(7):
        day={}
        # 早餐和加餐不用protein2
        day["早餐"]=allocate_meal(bf_pool[i%len(bf_pool)], protein_g*protein_dist["早餐"], calories_per_day*0.25, allow_protein2=False)
        day["加餐"]=allocate_meal(s_pool[i%len(s_pool)], protein_g*protein_dist["加餐"], calories_per_day*0.15, allow_protein2=False)

        # 午餐
        meal_l = l_pool[i%len(l_pool)].copy()
        available_p2 = [p for p in protein2_options if p not in protein2_used and p != meal_l["protein"]]
        if available_p2:
            meal_l["protein2"]=available_p2[0]
            protein2_used.append(available_p2[0])
        else:
            meal_l["protein2"]=None
        day["午餐"]=allocate_meal(meal_l, protein_g*protein_dist["午餐"], calories_per_day*0.3, allow_protein2=True)

        # 晚餐
        meal_d = d_pool[i%len(d_pool)].copy()
        # 确保晚餐 protein 不与午餐 protein 重复
        if meal_d["protein"] == meal_l["protein"]:
            meal_d["protein"]=random.choice([p for p in food_db if food_db[p]["type"]=="protein" and p != meal_l["protein"]])
        available_p2 = [p for p in protein2_options if p not in protein2_used and p != meal_d["protein"]]
        if available_p2:
            meal_d["protein2"]=available_p2[0]
            protein2_used.append(available_p2[0])
        else:
            meal_d["protein2"]=None
        day["晚餐"]=allocate_meal(meal_d, protein_g*protein_dist["晚餐"], calories_per_day*0.3, allow_protein2=True)

        week.append(day)
    return week

# ---------------- 显示一周概要 ----------------
def generate_week_summary(week):
    summary=[]
    for idx,day in enumerate(week,1):
        row={"天数":f"第{idx}天"}
        for meal_name,meal in day.items():
            items,cal,p,c,f = meal
            row[f"{meal_name}热量"]=cal
            row[f"{meal_name}蛋白"]=p
            row[f"{meal_name}碳水"]=c
            row[f"{meal_name}脂肪"]=f
        summary.append(row)
    return pd.DataFrame(summary)

if st.button("生成一周健康餐"):
    week = generate_week_menu(breakfast_pool,lunch_pool,dinner_pool,snack_pool,protein_g,calories_per_day)

    st.subheader("📅 一周菜单概要")
    st.dataframe(generate_week_summary(week))

    for idx,day in enumerate(week,1):
        with st.expander(f"第{idx}天菜单"):
            for meal_name, meal in day.items():
                items, cal, p, c, f = meal
                meal_text=[f"{name} {g}g" for name,g,_,_,_,_ in items]
                st.markdown(f"**{meal_name}**: {', '.join(meal_text)} | 热量: {cal} kcal, 蛋白质: {p} g, 碳水: {c} g, 脂肪: {f} g")
