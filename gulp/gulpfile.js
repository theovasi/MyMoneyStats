'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');

gulp.task('default', function() {
    ;
});

gulp.task('sass', function () {
    return gulp.src('../assets/styles/**/*.scss')
        .pipe(sourcemaps.init())
        .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
        .pipe(sourcemaps.write('maps/'))
        .pipe(gulp.dest('../static/dist'));
});

gulp.task('watch', function () {
    gulp.watch('../assets/styles/**/*.scss', ['sass']);
});
