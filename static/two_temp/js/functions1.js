$(function (){
 // Custom Navigation 
 $(".post-next").click(function(){
  itemSlider.trigger('owl.next');
});
 $(".post-prev").click(function(){
  itemSlider.trigger('owl.prev');
});


});

  /*------------------------------ SmoothScroll (for Mouse Wheel) v1.2.1 ----------------------*/
  (function ($) {
    var defaultOptions = {
      frameRate: 150,
      animationTime: 1200,
      stepSize: 120,
      pulseAlgorithm: !0,
      pulseScale: 8,
      pulseNormalize: 1,
      accelerationDelta: 20,
      accelerationMax: 1
    }, options = defaultOptions,
    direction = {
      x: 0,
      y: 0
    }, root = 0 <= document.compatMode.indexOf("CSS") || !document.body ? document.documentElement : document.body,
    que = [],
    pending = !1,
    lastScroll = +new Date;

    function scrollArray(a, b, c, d) {
      d || (d = 1E3);
      directionCheck(b, c);
      if (1 != options.accelerationMax) {
        var e = +new Date - lastScroll;
        e < options.accelerationDelta && (e = (1 + 30 / e) / 2, 1 < e && (e = Math.min(e, options.accelerationMax), b *= e, c *= e));
        lastScroll = +new Date
      }
      que.push({
        x: b,
        y: c,
        lastX: 0 > b ? 0.99 : -0.99,
        lastY: 0 > c ? 0.99 : -0.99,
        start: +new Date
      });
      if (!pending) {
        var q = a === document.body,
        p = function (e) {
          e = +new Date;
          for (var h = 0, k = 0, l = 0; l < que.length; l++) {
            var f = que[l],
            m = e - f.start,
            n = m >= options.animationTime,
            g = n ? 1 : m / options.animationTime;
            options.pulseAlgorithm && (g = pulse(g));
            m = f.x * g - f.lastX >> 0;
            g = f.y * g - f.lastY >> 0;
            h += m;
            k += g;
            f.lastX += m;
            f.lastY += g;
            n && (que.splice(l, 1), l--)
          }
          q ? window.scrollBy(h, k) : (h && (a.scrollLeft += h), k && (a.scrollTop += k));
          b || c || (que = []);
          que.length ? requestFrame(p, a, d / options.frameRate + 1) : pending = !1
        };
        requestFrame(p, a, 0);
        pending = !0
      }
    }

    function wheel(a) {
      var b = overflowingAncestor(a.target);
      if (!b || a.defaultPrevented) return !0;
      var c = a.wheelDeltaX || 0,
      d = a.wheelDeltaY || 0;
      c || d || (d = a.wheelDelta || 0);
      1.2 < Math.abs(c) && (c *= options.stepSize / 120);
      1.2 < Math.abs(d) && (d *= options.stepSize / 120);
      scrollArray(b, -c, -d);
      a.preventDefault()
    }
    var cache = {};
    setInterval(function () {
      cache = {}
    }, 1E4);
    var uniqueID = function () {
      var a = 0;
      return function (b) {
        return b.uniqueID || (b.uniqueID = a++)
      }
    }();

    function setCache(a, b) {
      for (var c = a.length; c--;) cache[uniqueID(a[c])] = b;
        return b
    }

    function overflowingAncestor(a) {
      var b = [],
      c = root.scrollHeight;
      do {
        var d = cache[uniqueID(a)];
        if (d) return setCache(b, d);
        b.push(a);
        if (c === a.scrollHeight) {
          if (root.clientHeight + 10 < c) return setCache(b, document.body)
        } else if (a.clientHeight + 10 < a.scrollHeight && (overflow = getComputedStyle(a, "").getPropertyValue("overflow-y"), "scroll" === overflow || "auto" === overflow)) return setCache(b, a)
    } while (a = a.parentNode)
  }

  function directionCheck(a, b) {
    a = 0 < a ? 1 : -1;
    b = 0 < b ? 1 : -1;
    if (direction.x !== a || direction.y !== b) direction.x = a, direction.y = b, que = [], lastScroll = 0
  }
var requestFrame = function () {
  return window.requestAnimationFrame || window.webkitRequestAnimationFrame || function (a, b, c) {
    window.setTimeout(a, c || 1E3 / 60)
  }
}();

function pulse_(a) {
  var b;
  a *= options.pulseScale;
  1 > a ? b = a - (1 - Math.exp(-a)) : (b = Math.exp(-1), a = 1 - Math.exp(-(a - 1)), b += a * (1 - b));
  return b * options.pulseNormalize
}

function pulse(a) {
  if (1 <= a) return 1;
  if (0 >= a) return 0;
  1 == options.pulseNormalize && (options.pulseNormalize /= pulse_(1));
  return pulse_(a)
}
window.addEventListener("mousewheel", wheel, !1);

})(jQuery);
