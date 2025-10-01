import streamlit as st
import random

st.set_page_config(page_title="健康餐助手", layout="wide")
st.title("🥗 健康餐助手 - 个性化一周计划 + 购物清单")

# 用户输入
height = st.number_input("身高 (cm)", 100, 250, 170)
weight = st.number_input("体重 (kg)", 30, 200, 65)
goal = st.selectbox("你的目标", ["减脂", "保持", "增肌"])

age = 25
gender = "男"

# 基础代谢率 (BMR)
if gender == "男":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

# 总热量按目标调整
if goal == "减脂":
    calories_per_day = int(bmr * 1.2)
elif goal == "保持":
    calories_per_day = int(bmr * 1.4)
else:
    calories_per_day = int(bmr * 1.6)

# 每日营养需求
protein_g = int(weight * 1.8)  # 蛋白质
fat_ratio = 0.25
carb_ratio = 0.5
fat_g = int(calories_per_day * fat_ratio / 9)
carb_g = int(calories_per_day * carb_ratio / 4)

st.subheader("📊 每日营养目标")
st.write(f"- 热量：{calories_per_day} kcal")
st.write(f"- 蛋白质：{protein_g} g")
st.write(f"- 碳水化合物：{carb_g} g")
st.write(f"- 脂肪：{fat_g} g")

# 食物库与营养信息 (每100g热量 kcal / 蛋白质 g / 碳水 g / 脂肪 g)
food_db = {
    "鸡胸肉": {"cal": 165, "p": 31, "c": 0, "f": 3.6},
    "牛肉": {"cal": 250, "p": 26, "c": 0, "f": 15},
    "三文鱼": {"cal": 208, "p": 20, "c": 0, "f": 13},
    "火鸡胸肉": {"cal": 135, "p": 29, "c": 0, "f": 1},
    "鸡蛋": {"cal": 155, "p": 13, "c": 1, "f": 11},
    "燕麦片": {"cal": 389, "p": 17, "c": 66, "f": 7},
    "糙米": {"cal": 111, "p": 2.6, "c": 23, "f": 0.9},
    "红薯": {"cal": 86, "p": 1.6, "c": 20, "f": 0.1},
    "西兰花": {"cal": 34, "p": 2.8, "c": 7, "f": 0.4},
    "菠菜": {"cal": 23, "p": 2.9, "c": 3.6, "f": 0.4},
    "芦笋": {"cal": 20, "p": 2.2, "c": 3.9, "f": 0.1},
    "四季豆": {"cal": 31, "p": 1.8, "c": 7, "f": 0.1},
    "玉米": {"cal": 86, "p": 3.2, "c": 19, "f": 1.2},
    "全麦面包": {"cal": 247, "p": 13, "c": 41, "f": 4},
    "坚果": {"cal": 607, "p": 20, "c": 21, "f": 54},
    "酸奶": {"cal": 59, "p": 10, "c": 3.6, "f": 0.4},
    "香蕉": {"cal": 89, "p": 1.1, "c": 23, "f": 0.3},
    "豆腐": {"cal": 76, "p": 8, "c": 1.9, "f": 4.8},
}

# 简单食物分类
breakfast_options = [["燕麦片", "牛奶", "鸡蛋"], ["全麦面包", "鸡蛋", "香蕉"], ["酸奶", "燕麦片", "香蕉"]]
lunch_options = [["鸡胸肉", "西兰花", "糙米"], ["牛肉", "红薯", "西兰花"], ["三文鱼", "菠菜", "藜麦"]]
dinner_options = [["鸡胸肉", "芦笋", "糙米"], ["三文鱼", "玉米", "红薯"], ["火鸡胸肉", "四季豆", "全麦面包"]]
snack_options = [["坚果", "香蕉"], ["酸奶", "水果"], ["蛋白棒"]]

# 生成一周菜单并按比例分配克数
week_meals = []
st.subheader("📅 一周饮食计划")
for day in range(1, 8):
    breakfast = random.choice(breakfast_options)
    lunch = random.choice(lunch_options)
    snack = random.choice(snack_options)
    dinner = random.choice(dinner_options)
    day_meals = [breakfast, lunch, snack, dinner]
    week_meals.append(day_meals)

    st.markdown(f"### 第 {day} 天")
    for meal_name, meal in zip(["早餐", "午餐", "加餐", "晚餐"], day_meals):
        # 简单分配，每餐热量按比例
        total_calories = calories_per_day / 4
        meal_display = []
        for food in meal:
            # 克数 = 目标热量 / 食物每100g热量 * 100
            g = max(10, int(total_calories / len(meal) / food_db.get(food, {"cal":50})["cal"] * 100))
            meal_display.append(f"{food} {g}g")
        st.write(f"**{meal_name}**：{', '.join(meal_display)}")
    st.write("---")

# 生成一周购物清单（累加每餐克数）
shopping_list = {}
for day_meals in week_meals:
    for meal in day_meals:
        total_calories = calories_per_day / 4
        for food in meal:
            g = max(10, int(total_calories / len(meal) / food_db.get(food, {"cal":50})["cal"] * 100))
            if food in shopping_list:
                shopping_list[food] += g
            else:
                shopping_list[food] = g

st.subheader("🛒 一周购物清单（总量）")
for food, total in shopping_list.items():
    st.write(f"- {food}: {total*7//len(week_meals)} g")
