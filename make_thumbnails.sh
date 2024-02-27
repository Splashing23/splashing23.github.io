for file in images/*.{jpg,jpeg,png}; do
    #[ ! -f "tn/$file" ] && 
    convert "$file" -resize 250x250 "tn/$file"
done

convert images/portrait_circle.jpg -resize 5000x5000 "tn/images/portrait_circle.jpg"