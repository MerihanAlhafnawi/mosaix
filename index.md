## Create collaborative art with robot tiles!



### Screen colour


<p>Choose the screen colour of your robot:</p>

<div>
    <input type="color" id="colour" name="colour" onchange="change_colour(this.value)"
           value="#e66465">
    <label for="head">Head</label>
</div>

<?php
$jsonString = file_get_contents('data/robots.json');
$data = json_decode($jsonString, true);
print ($data);
?>

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/MerihanAlhafnawi/mosaix/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
