-- First, delete existing data
DELETE FROM bookmodule_student_courses;  -- Delete from many-to-many relationship table first
DELETE FROM bookmodule_student;
DELETE FROM bookmodule_card;
DELETE FROM bookmodule_department;
DELETE FROM bookmodule_course;

-- Insert departments
INSERT INTO bookmodule_department (name) VALUES
('Computer Science'),
('Information Technology'),
('Software Engineering'),
('Cybersecurity'),
('Data Science');

-- Insert courses
INSERT INTO bookmodule_course (title, code) VALUES
('Introduction to Programming', 101),
('Database Systems', 201),
('Web Development', 301),
('Artificial Intelligence', 401),
('Network Security', 501),
('Data Structures', 202),
('Machine Learning', 402),
('Cloud Computing', 302);

-- Insert cards with numbers
INSERT INTO bookmodule_card (card_number) VALUES
(200001),
(200002),
(200003),
(200004),
(200005),
(200006),
(200007),
(200008);

-- Insert students with departments and cards
INSERT INTO bookmodule_student (name, age, address_id, card_id, department_id) VALUES
('محمد العتيبي', 20, (SELECT id FROM bookmodule_address WHERE city='Riyadh'), 
    (SELECT id FROM bookmodule_card WHERE card_number=200001),
    (SELECT id FROM bookmodule_department WHERE name='Computer Science')),
('أحمد القحطاني', 21, (SELECT id FROM bookmodule_address WHERE city='Jeddah'),
    (SELECT id FROM bookmodule_card WHERE card_number=200002),
    (SELECT id FROM bookmodule_department WHERE name='Information Technology')),
('سارة الغامدي', 19, (SELECT id FROM bookmodule_address WHERE city='Dammam'),
    (SELECT id FROM bookmodule_card WHERE card_number=200003),
    (SELECT id FROM bookmodule_department WHERE name='Software Engineering')),
('فاطمة السهلي', 22, (SELECT id FROM bookmodule_address WHERE city='Makkah'),
    (SELECT id FROM bookmodule_card WHERE card_number=200004),
    (SELECT id FROM bookmodule_department WHERE name='Cybersecurity')),
('عبدالله الدوسري', 20, (SELECT id FROM bookmodule_address WHERE city='Madinah'),
    (SELECT id FROM bookmodule_card WHERE card_number=200005),
    (SELECT id FROM bookmodule_department WHERE name='Data Science')),
('نورة الشهري', 21, (SELECT id FROM bookmodule_address WHERE city='Riyadh'),
    (SELECT id FROM bookmodule_card WHERE card_number=200006),
    (SELECT id FROM bookmodule_department WHERE name='Computer Science')),
('خالد المالكي', 23, (SELECT id FROM bookmodule_address WHERE city='Jeddah'),
    (SELECT id FROM bookmodule_card WHERE card_number=200007),
    (SELECT id FROM bookmodule_department WHERE name='Information Technology')),
('ريم الزهراني', 20, (SELECT id FROM bookmodule_address WHERE city='Makkah'),
    (SELECT id FROM bookmodule_card WHERE card_number=200008),
    (SELECT id FROM bookmodule_department WHERE name='Software Engineering'));

-- Insert student-course relationships
INSERT INTO bookmodule_student_courses (student_id, course_id)
SELECT s.id, c.id
FROM bookmodule_student s
CROSS JOIN bookmodule_course c
WHERE 
    (s.department_id = (SELECT id FROM bookmodule_department WHERE name='Computer Science') 
     AND c.code IN (101, 201, 301))
    OR
    (s.department_id = (SELECT id FROM bookmodule_department WHERE name='Information Technology')
     AND c.code IN (201, 301, 501))
    OR
    (s.department_id = (SELECT id FROM bookmodule_department WHERE name='Software Engineering')
     AND c.code IN (101, 202, 302))
    OR
    (s.department_id = (SELECT id FROM bookmodule_department WHERE name='Cybersecurity')
     AND c.code IN (501, 301, 202))
    OR
    (s.department_id = (SELECT id FROM bookmodule_department WHERE name='Data Science')
     AND c.code IN (402, 202, 201));