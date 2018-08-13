'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var pump = require('pump');
var uglify = require('gulp-uglify-es').default;

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

gulp.task('uglify', function (cb) {
    pump([
        gulp.src('../assets/scripts/*.js'), 
        uglify(), gulp.dest('../static/dist')], 
        cb);
});

gulp.task('watch', function () {
    gulp.watch('../assets/styles/**/*.scss', ['sass']);
    gulp.watch('../assets/scripts/*.js', ['uglify']);
});
