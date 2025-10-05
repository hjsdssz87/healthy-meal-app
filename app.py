import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="智能营养餐助手（带每日详情）", layout="centered")
st.title("🥗 智能营养餐助手（中西结合，一周概要+每日详情）")
st.caption("根据 性别/年龄/身高/体重/目标 自动生成一周菜单、概要表与每日详情")

# -------------------------
# 用户输入
# -------------------------
col1, col2, col3 = st.columns(3)
with col1:
    height = st.number_input("身高 (cm)", min_value=100, max_value=250, value=170)
with col2:
    weight = st.number_input("体重 (kg)", min_value=30, max_value=200, value=65)
with col3:
    age = st.number_input("年龄", min_value=10, max_value=100, value=25)

gender = st.selectbox("性别", ["男", "女"])
goal = st.selectbox("目标", ["减脂", "保持", "增肌"])

# -------------------------
# 计算每日目标
# -------------------------
if gender == "男":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

factor = 1.2 if goal == "减脂" else 1.4 if goal == "保持" else 1.6
sex_adj = 1.05 if gender == "男" else 0.95
calories_per_day = int(bmr * factor * sex_adj)
protein_g = int(weight * (1.8 if gender == "男" else 1.6))
fat_g = int(calories_per_day * 0.25 / 9)
carb_g = int(calories_per_day * 0.5 / 4)

st.markdown(f"**每日营养目标**：热量 {calories_per_day} kcal ｜ 蛋白质 {protein_g} g ｜ 碳水 {carb_g} g ｜ 脂肪 {fat_g} g")

# -------------------------
# 食物库（中西结合）
# -------------------------
food_db = {
    "鸡胸肉":{"cal":165,"p":31,"c":0,"f":3.6},"鸡腿肉":{"cal":209,"p":26,"c":0,"f":11},
    "牛肉":{"cal":250,"p":26,"c":0,"f":15},"猪里脊":{"cal":242,"p":27,"c":0,"f":14},
    "三文鱼":{"cal":208,"p":20,"c":0,"f":13},"鳕鱼":{"cal":82,"p":18,"c":0,"f":0.7},
    "虾仁":{"cal":99,"p":24,"c":0.2,"f":0.3},"金枪鱼罐头":{"cal":132,"p":28,"c":0,"f":1},
    "豆腐":{"cal":76,"p":8,"c":1.9,"f":4.8},"鸡蛋":{"cal":155,"p":13,"c":1,"f":11},
    "燕麦片":{"cal":389,"p":17,"c":66,"f":7},"糙米":{"cal":111,"p":2.6,"c":23,"f":0.9},
    "白米饭":{"cal":130,"p":2.4,"c":28,"f":0.3},"红薯":{"cal":86,"p":1.6,"c":20,"f":0.1},
    "全麦面包":{"cal":247,"p":13,"c":41,"f":4.2},"藜麦":{"cal":120,"p":4.1,"c":21,"f":1.9},
    "意大利面":{"cal":131,"p":5,"c":25,"f":1.1},"土豆":{"cal":77,"p":2,"c":17,"f":0.1},
    "西兰花":{"cal":55,"p":3.7,"c":11,"f":0.6},"菠菜":{"cal":23,"p":2.9,"c":3.6,"f":0.4},
    "芦笋":{"cal":20,"p":2.2,"c":3.9,"f":0.1},"四季豆":{"cal":31,"p":1.8,"c":7,"f":0.1},
    "胡萝卜":{"cal":41,"p":0.9,"c":10,"f":0.2},"番茄":{"cal":18,"p":0.9,"c":3.9,"f":0.2},
    "黄瓜":{"cal":16,"p":0.7,"c":3.6,"f":0.1},"蘑菇":{"cal":22,"p":3.1,"c":3.3,"f":0.3},
    "青椒":{"cal":20,"p":0.9,"c":4.6,"f":0.2},"香蕉":{"cal":89,"p":1.1,"c":23,"f":0.3},
    "苹果":{"cal":52,"p":0.3,"c":14,"f":0.2},"蓝莓":{"cal":57,"p":0.7,"c":14,"f":0.3},
    "草莓":{"cal":33,"p":0.7,"c":8,"f":0.3},"橙子":{"cal":47,"p":0.9,"c":12,"f":0.1},
    "猕猴桃":{"cal":61,"p":1.1,"c":15,"f":0.5},"葡萄":{"cal":69,"p":0.7,"c":18,"f":0.2},
    "坚果":{"cal":607,"p":20,"c":21,"f":54},"牛油果":{"cal":160,"p":2,"c":9,"f":15},
    "橄榄油":{"cal":884,"p":0,"c":0,"f":100},"酸奶":{"cal":59,"p":10,"c":3.6,"f":0.4},
    "低脂牛奶":{"cal":42,"p":3.4,"c":5,"f":1},"蛋白棒":{"cal":250,"p":20,"c":23,"f":7},
    "花生酱":{"cal":588,"p":25,"c":20,"f":50}
}

# -------------------------
# 每餐食物组合池（7种）
# -------------------------
breakfast_pool = [
    ["燕麦片","酸奶","香蕉"],["全麦面包","鸡蛋","苹果"],["燕麦片","低脂牛奶","蓝莓"],
    ["全麦面包","花生酱","香蕉"],["鸡蛋","全麦面包","橙子"],["燕麦片","酸奶","草莓"],
    ["蛋白棒","低脂牛奶","苹果"]
]
lunch_pool = [
    ["鸡胸肉","糙米","西兰花"],["三文鱼","藜麦","菠菜"],["牛肉","土豆","四季豆"],
    ["虾仁","意大利面","番茄"],["金枪鱼罐头","白米饭","黄瓜"],["猪里脊","红薯","胡萝卜"],
    ["豆腐","糙米","蘑菇"]
]
dinner_pool = [
    ["鳕鱼","菠菜","红薯"],["火鸡胸肉","芦笋","糙米"],["豆腐","蘑菇","全麦面包"],
    ["鸡腿肉","西兰花","土豆"],["三文鱼","青椒","藜麦"],["牛肉","菠菜","土豆"],
    ["虾仁","番茄","全麦面包"]
]
snack_pool_fatloss = [
    ["酸奶","蓝莓"],["胡萝卜","黄瓜"],["苹果","坚果"],["草莓","酸奶"],
    ["猕猴桃","坚果"],["香蕉","低脂牛奶"],["酸奶","葡萄"]
]
snack_pool_maintain = [
    ["酸奶","香蕉"],["坚果","苹果"],["蛋白棒","低脂牛奶"],["酸奶","蓝莓"],
    ["花生酱","全麦面包"],["牛油果","吐司"],["酸奶","草莓"]
]
snack_pool_gain = [
    ["蛋白棒","牛油果"],["花生酱","全麦面包"],["坚果","酸奶"],["蛋白棒","低脂牛奶"],
    ["花生酱","全麦面包"],["坚果","香蕉"],["牛油果","蛋白棒"]
]
snack_pool = snack_pool_fatloss if goal=="减脂" else snack_pool_gain if goal=="增肌" else snack_pool_maintain

meal_ratios = {"早餐":0.25,"午餐":0.35,"晚餐":0.25,"加餐":0.15}
gender_factor = 1.1 if gender=="男" else 0.9

def recommend_grams(food_key,target_cal):
    info = food_db.get(food_key)
    cal100 = info["cal"] if info else 100
    return int(max(20, target_cal / cal100 * 100))

def generate_day_plan():
    day = {}
    for meal_name, ratio in meal_ratios.items():
        meal_cal_target = calories_per_day * ratio
        if meal_name=="早餐":
            choice = random.choice(breakfast_pool)
        elif meal_name=="午餐":
            choice = random.choice(lunch_pool)
        elif meal_name=="晚餐":
            choice = random.choice(dinner_pool)
        else:
            choice = random.choice(snack_pool)
        per_item_cal = meal_cal_target / len(choice) * gender_factor
        items=[]
        sum_cal=sum_p=sum_c=sum_f=0
        for food in choice:
            grams = recommend_grams(food, per_item_cal)
            info = food_db.get(food)
            if info:
                cal = info["cal"]*grams/100
                p = info["p"]*grams/100
                c = info["c"]*grams/100
                f = info["f"]*grams/100
            else:
                cal=p=c=f=0
            items.append((food, grams, int(cal), int(p), int(c), int(f)))
            sum_cal+=cal; sum_p+=p; sum_c+=c; sum_f+=f
        day[meal_name] = {"items":items,"cal":int(sum_cal),"p":int(sum_p),"c":int(sum_c),"f":int(sum_f)}
    return day

# -------------------------
# 主体：一周概要 + 可展开详情
# -------------------------
if st.button("生成一周菜单"):
    week = [generate_day_plan() for _ in range(7)]

    rows=[]
    for i,day in enumerate(week,1):
        total_cal=sum([m["cal"] for m in day.values()])
        total_p=sum([m["p"] for m in day.values()])
        total_c=sum([m["c"] for m in day.values()])
        total_f=sum([m["f"] for m in day.values()])
        summary_items=[day[m]["items"][0][0] for m in ["早餐","午餐","晚餐","加餐"]]
        rows.append({
            "第几天":f"第 {i} 天","总热量(kcal)":int(total_cal),
            "蛋白质(g)":int(total_p),"碳水(g)":int(total_c),"脂肪(g)":int(total_f),
            "主要菜品": " / ".join(summary_items)
        })
    df=pd.DataFrame(rows)
    st.subheader("📊 一周概要")
    st.dataframe(df, use_container_width=True)

    # ---- 展开每日详情 ----
    st.subheader("📅 每日详情")
    for i,day in enumerate(week,1):
        with st.expander(f"第 {i} 天 菜单详情 ▼"):
            for meal_name,meal in day.items():
                st.markdown(f"**🍽️ {meal_name}** — 热量 {meal['cal']} kcal | 蛋白质 {meal['p']}g | 碳水 {meal['c']}g | 脂肪 {meal['f']}g")
                df_meal = pd.DataFrame(meal["items"], columns=["食物","克数","热量","蛋白质","碳水","脂肪"])
                st.dataframe(df_meal, use_container_width=True)

    # ---- 周购物清单 ----
    shopping={}
    for day in week:
        for meal in day.values():
            for food,grams,*_ in meal["items"]:
                shopping[food]=shopping.get(food,0)+grams
    st.subheader("🛒 一周购物清单")
    for k,v in shopping.items():
        st.markdown(f"- {k}: {v} g（约 {int(v/100)} 份 100g）")

    st.success("✅ 一周菜单生成完成，可展开查看每日详情。")
