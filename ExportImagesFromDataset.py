import argparse
import mysql.connector as mysql
from PIL import Image


def overlap(rec1, rec2):
    return not (rec1[3] <= rec2[1] or
                rec1[4] <= rec2[2] or
                rec1[1] >= rec2[3] or
                rec1[2] >= rec2[4])


def size(rec):
    return (rec[3] - rec[1]) * (rec[4] - rec[2])


def is_rec_inside(larger, smaller):
    return ((smaller[1] > larger[1]) and
            (smaller[2] > larger[2]) and
            (smaller[3] < larger[3]) and
            (smaller[4] < larger[4]))


def is_rec_overlapping(rectangles):
    for i in range(len(rectangles)):
        for j in range(i, len(rectangles)):
            if i == j:
                continue
            if overlap(rectangles[i], rectangles[j]):
                return True
    return False


def add_to_dictionary(records):
    record_dic = {}
    for box in records:
        if not box[0] in record_dic:
            record_dic[box[0]] = []
        record_dic[box[0]].append(box)
    return record_dic


def resize_and_save(input_path, output_path, name, save_name, start_x, start_y, end_x, end_y, resize_width,
                    resize_height, image_aspect):
    image_object = Image.open(input_path + name)
    width, height = image_object.size

    center_x = ((end_x - start_x) / 2) + start_x
    center_y = ((end_y - start_y) / 2) + start_y

    width_x = end_x - start_x
    width_y = end_y - start_y
    box_aspect = width_x / width_y

    if image_aspect < box_aspect:
        width_y = round(width_x / image_aspect)
    elif image_aspect > box_aspect:
        width_x = round(width_y * image_aspect)

    crop_start_x = center_x - width_x / 2
    crop_end_x = center_x + width_x / 2

    crop_start_y = center_y - width_y / 2
    crop_end_y = center_y + width_y / 2

    if crop_start_x < 0:
        crop_start_x = 0
    if crop_end_x > width:
        crop_end_x = width

    if crop_start_y < 0:
        crop_start_y = 0
    if crop_end_y > height:
        crop_end_y = height

    cropped = image_object.crop((crop_start_x, crop_start_y, crop_end_x, crop_end_y))
    img = cropped.resize((resize_width, resize_height), Image.ANTIALIAS)
    img.save(output_path + save_name)


def process_single_box(args, cursor, aspect):
    single_box_sql = """SELECT DISTINCT b.imageId, b.startX, b.startY, b.endX, b.endY, b.categoryId, images.filename
                        FROM images INNER JOIN 
                             boxes AS b ON b.imageId = images.id
                        WHERE images.id IN 
                        (SELECT DISTINCT boxes.imageId 
                        FROM boxes 
                        GROUP BY boxes.imageId
                        HAVING COUNT(boxes.Id) = 1
                        )
                        AND b.categoryId = 4 LIMIT 10000;"""
    print('Fetching single box images from database...')
    cursor.execute(single_box_sql)
    records = cursor.fetchall()
    print('Cropping images...')
    count = 0
    for image in records:
        if not ((image[3] - image[1]) < args.width or (image[4] - image[2]) < args.height):
            resize_and_save(args.dataset_dir, args.output_dir, image[6], image[6], image[1], image[2],
                            image[3], image[4], args.width, args.height, aspect)
        count += 1
        if count % 1000 == 0 and count != 0:
            print('Finished', count, 'single box images')
    return count


def process_multiple_boxes(args, cursor, aspect):
    multiple_box_sql = """SELECT DISTINCT b.imageId, b.startX, b.startY, b.endX, b.endY, b.categoryId, images.filename
                        FROM images INNER JOIN 
                             boxes AS b ON b.imageId = images.id
                        WHERE images.id IN 
                        (SELECT DISTINCT boxes.imageId 
                        FROM boxes 
                        GROUP BY boxes.imageId
                        HAVING COUNT(boxes.Id) > 1) LIMIT 10000;"""
    print('Fetching multiple box images from database...')
    cursor.execute(multiple_box_sql)
    records = cursor.fetchall()

    print('Adding images to dictionary...')
    record_dic = add_to_dictionary(records)
    print('Cropping images...')
    count = 0
    for record in record_dic:
        filtered = record_dic[record]
        if not is_rec_overlapping(filtered):
            cars_only = filter(lambda x: x[5] == 4, filtered)
            for car in cars_only:
                start_x = int(car[1])
                start_y = int(car[2])
                end_x = int(car[3])
                end_y = int(car[4])
                if not ((end_x - start_x) < args.width or (end_y - start_y) < args.height):
                    resize_and_save(args.dataset_dir, args.output_dir, filtered[0][6], filtered[0][6], start_x,
                                    start_y, end_x, end_y, args.width, args.height, aspect)
                    count += 1
        if count % 1000 == 0 and count != 0:
            print('Finished', count, 'multiple box images')
    return count


def process_multiple_box_overlapping_person(args, cursor, aspect):
    two_box_sql = """SELECT DISTINCT b.imageId, b.startX, b.startY, b.endX, b.endY, b.categoryId, images.filename
                        FROM images INNER JOIN 
                             boxes AS b ON b.imageId = images.id
                        WHERE images.id IN 
                        (SELECT DISTINCT boxes.imageId 
                        FROM boxes 
                        GROUP BY boxes.imageId
                        HAVING COUNT(boxes.Id) = 2) LIMIT 10000;"""
    print('Fetching images with 2 boxes from database...')
    cursor.execute(two_box_sql)
    records = cursor.fetchall()

    print('Adding images to dictionary...')
    record_dic = add_to_dictionary(records)
    print('Cropping images...')

    count = 0
    for record in record_dic:
        filtered = record_dic[record]

        if size(filtered[0]) > size(filtered[1]):
            larger = filtered[0]
            smaller = filtered[1]
        else:
            larger = filtered[1]
            smaller = filtered[0]

        if is_rec_inside(larger, smaller) and larger[5] == 4 and smaller[5] == 2:
            start_x = int(larger[1])
            start_y = int(larger[2])
            end_x = int(larger[3])
            end_y = int(larger[4])
            if not ((end_x - start_x) < args.width or (end_y - start_y) < args.height):
                resize_and_save(args.dataset_dir, args.output_dir, larger[6], larger[6], start_x,
                                start_y, end_x, end_y, args.width, args.height, aspect)
                count += 1
            if count % 1000 == 0 and count != 0:
                print('Finished', count, 'images with 2 boxes')
    return count


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_dir', dest='dataset_dir', help='Path to dataset directory',  required=True)
    parser.add_argument('--width', dest='width', type=int, help='Preferred image width in pixels', required=True)
    parser.add_argument('--height', dest='height', type=int, help='Preferred image height in pixels', required=True)
    parser.add_argument('--host', dest='host', help='MySQL host address', required=True)
    parser.add_argument('--username', dest='username', help='MySQL username', required=True)
    parser.add_argument('--password', dest='password', help='MySQL password', required=True)
    parser.add_argument('--database', dest='database', help='MySQL database name', required=True)
    parser.add_argument('--output_dir', dest='output_dir', help='Path to output directory', required=True)
    parser.add_argument('--single_box', dest='single_box', type=bool, help='Output images with single box of car',
                        required=True)
    parser.add_argument('--multiple_box', dest='multiple_box', type=bool,
                        help='Output images with multiple boxes of non overlapping car', required=True)
    parser.add_argument('--multiple_box_overlapping_person', dest='multiple_box_overlapping_person', type=bool,
                        help='Output images with persons in cars', required=True)
    args = parser.parse_args()

    db = mysql.connect(
        host=args.host,
        user=args.username,
        passwd=args.password,
        database=args.database
    )
    cursor = db.cursor()

    aspect = args.height / args.width
    single_count = 0
    multiple_count = 0
    person_count = 0
    if args.single_box:
        single_count = process_single_box(args, cursor, aspect)
    if args.multiple_box:
        multiple_count = process_multiple_boxes(args, cursor, aspect)
    if args.multiple_box_overlapping_person:
        person_count = process_multiple_box_overlapping_person(args, cursor, aspect)

    print('Finished! Extracted total', single_count + multiple_count + person_count, 'images.')
    print('Single box images:', single_count)
    print('Multiple box images:', multiple_count)
    print('Multiple box images with persons in cars:', person_count)


if __name__ == '__main__':
    start()
