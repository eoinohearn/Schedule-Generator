from app import app, db, main, Course_database
app.app_context().push()

df = main.pd.read_excel(r'C:\Users\drags\OneDrive\Desktop\Programacion\Personal\ClassScheduling\ClassListExcel.xlsx')
df = df.fillna("empty")
updated_list = main.make_Total_Classes_List(df)

for course in updated_list:
    preReq_string = ''
    coReq_string = ''
    for i in course.preReq:
        preReq_string += i + ' '
    for i in course.coReq:
        coReq_string += i + ' '
    new_course_db = Course_database(name = course.name, credits = course.credits, preReq = preReq_string, coReq = coReq_string)

    check_course = Course_database.query.filter_by(name = course.name).first()

    if check_course:
        continue

    else:
        db.session.add(new_course_db)
        db.session.commit()


print('Done')