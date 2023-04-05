/**
 ## JavaScript Doc
 You can describe file here.

 And you can use here any Markdown syntax.

 ### Usage
 ```bash
 hapdoc build yourJsProject -d js
 ```
 Here, `-d js` is shortcut of `--doctype js`

 ### Good Luck 🙂
*/


/**
 * Provides Rectangle class
 * 
 * @class Rectangle
 */
class Rectangle {
  x = 0.0;
  y = 0.0;
  w = 1.0;
  h = 1.0;

  /**
   * Creates a new Rectangle object
   * 
   * @param {Number} x left corner of Rectangle
   * @param {Number} y top corner of Rectangle
   * @param {Number} w width of Rectangle
   * @param {Number} h height of Rectangle
   */
  constructor(x, y, w, h) {
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
  }

  /**
   * Calculates rectangle area
   * 
   * @memberof Rectangle
   * @return {Number} Area of rectangle
   */
  area() {
    return this.w * this.h;
  }
}

/**
 * Calculates sum of `a` and `b`
 * 
 * @param {Number} a left
 * @param {Number} b right
 * @return {Number} sum of `a` and `b`
 */
function sum(a, b) {
  return a + b;
}


let rect = new Rectangle(1, 2, 3, 4);
console.log(rect);
console.log(rect.area());
