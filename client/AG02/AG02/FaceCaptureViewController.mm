//
//  FaceCaptureViewController.m
//  AG02
//
//  Created by デービット スクリプス on 8/2/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "UIImage+OpenCV.h"

#import "FaceCaptureViewController.h"
#import "CaptureConfirmViewController.h"

#import <AudioToolbox/AudioToolbox.h>

// Name of face cascade resource file without xml extension
NSString * const kFaceCascadeFilename = @"haarcascade_frontalface_alt2";
NSString * const kEyeCascadeFilename = @"haarcascade_eye";

// Options for cv::CascadeClassifier::detectMultiScale
const int kHaarOptions =  CV_HAAR_FIND_BIGGEST_OBJECT | CV_HAAR_DO_ROUGH_SEARCH;

@interface FaceCaptureViewController ()
- (void)displayFaces:(const std::vector<cv::Rect> &)faces 
        forVideoRect:(CGRect)rect 
    videoOrientation:(AVCaptureVideoOrientation)videoOrientation;
@end

@implementation FaceCaptureViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        self.captureGrayscale = YES;
        self.qualityPreset = AVCaptureSessionPresetMedium;
    }
    return self;
}

#pragma mark - View lifecycle

- (void)viewDidLoad
{
    [super viewDidLoad];
    
    //add face image later
    faceImage = nil;
    
    // Load the face Haar cascade from resources
    NSString *faceCascadePath = [[NSBundle mainBundle] pathForResource:kFaceCascadeFilename ofType:@"xml"];
    
    if (!_faceCascade.load([faceCascadePath UTF8String])) {
        NSLog(@"Could not load face cascade: %@", faceCascadePath);
    }
    
    NSString *eyeCascadePath = [[NSBundle mainBundle] pathForResource:kEyeCascadeFilename ofType:@"xml"];
    if (!_eyeCascade.load([eyeCascadePath UTF8String])) {
        NSLog(@"Could not load eye cascade: %@", eyeCascadePath);
    }
    

}

- (void)viewDidUnload
{
    [super viewDidUnload];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

// MARK: IBActions

// Toggles display of FPS
- (IBAction)toggleFps:(id)sender
{
    self.showDebugInfo = !self.showDebugInfo;
}

// Turn torch on and off
- (IBAction)toggleTorch:(id)sender
{
    self.torchOn = !self.torchOn;
}

// Switch between front and back camera
- (IBAction)toggleCamera:(id)sender
{
    if (self.camera == 1) {
        self.camera = 0;
    }
    else
    {
        self.camera = 1;
    }
}

// MARK: After face captured

- (void)gotoConfirm
{
    if(start == nil) {
        start = [[NSDate date] retain];
    }
    //note the time (give user a few seconds before checking faces)
    NSTimeInterval secondsElapsed = [[NSDate date] timeIntervalSinceDate:start];
    if (secondsElapsed < 1) {
        return;
    }
    
    
    if(faceImage != nil) {
        //already got the face, finished
        return;
    }
    //note that this is the face image we want
    faceImage = currentImage;
    //vibrate phone
    AudioServicesPlaySystemSound(kSystemSoundID_Vibrate);
    //go to confirmation screen after a delay
    [self performSelector:@selector(openNewView) withObject:nil];

}

- (void)openNewView 
{
    
    CaptureConfirmViewController *vC = [[[CaptureConfirmViewController alloc] initWithNibName:@"CaptureConfirmViewController" bundle:nil] autorelease];
    //vC.modalTransitionStyle = UIModalTransitionStyleCrossDissolve;
    [vC initStuff:faceImage camera:self.camera];
    [self presentModalViewController:vC animated:NO];
    
    
    //TODO correctly destroy this view controller
    [super viewDidUnload];
     
}


// MARK: VideoCaptureViewController overrides

- (void)processFrame:(cv::Mat &)mat img:(UIImage*)img videoRect:(CGRect)rect videoOrientation:(AVCaptureVideoOrientation)videOrientation
{
    
    //track the current image in case we need it
    currentImage = img;
    
    // Shrink video frame to 320X240
    cv::resize(mat, mat, cv::Size(), 0.5f, 0.5f, CV_INTER_LINEAR);
    rect.size.width /= 2.0f;
    rect.size.height /= 2.0f;
    
    // Rotate video frame by 90deg to portrait by combining a transpose and a flip
    // Note that AVCaptureVideoDataOutput connection does NOT support hardware-accelerated
    // rotation and mirroring via videoOrientation and setVideoMirrored properties so we
    // need to do the rotation in software here.
    cv::transpose(mat, mat);
    CGFloat temp = rect.size.width;
    rect.size.width = rect.size.height;
    rect.size.height = temp;
    
    if (videOrientation == AVCaptureVideoOrientationLandscapeRight)
    {
        // flip around y axis for back camera
        cv::flip(mat, mat, 1);
    }
    else {
        // Front camera output needs to be mirrored to match preview layer so no flip is required here
    }
    
    videOrientation = AVCaptureVideoOrientationPortrait;
    
    // Detect faces
    std::vector<cv::Rect> faces;
    
    _faceCascade.detectMultiScale(mat, faces, 1.1, 2, kHaarOptions, cv::Size(60, 60));
    
    
    // Dispatch updating of face markers to main queue
    dispatch_sync(dispatch_get_main_queue(), ^{
        [self displayFaces:faces forMat:mat forVideoRect:rect videoOrientation:videOrientation];
    });
     
}

- (void)drawHaarObject:(cv::Rect)haarObject
{
    
}

// Update face markers given vector of face rectangles
- (void)displayFaces:(const std::vector<cv::Rect> &)faces 
    forMat:(cv::Mat)mat
    forVideoRect:(CGRect)rect 
    videoOrientation:(AVCaptureVideoOrientation)videoOrientation
{
    
    if(faces.size() < 1) {
        start = nil;//reset time
        return;
    }
    
    NSArray *sublayers = [NSArray arrayWithArray:[self.view.layer sublayers]];
    int sublayersCount = [sublayers count];
    int currentSublayer = 0;
    
	[CATransaction begin];
	[CATransaction setValue:(id)kCFBooleanTrue forKey:kCATransactionDisableActions];
	
	// hide all the face layers
	for (CALayer *layer in sublayers) {
        NSString *layerName = [layer name];
		if ([layerName isEqualToString:@"FaceLayer"])
			[layer setHidden:YES];
		if ([layerName isEqualToString:@"LeftEyeLayer"])
			[layer setHidden:YES];
		if ([layerName isEqualToString:@"RightEyeLayer"])
			[layer setHidden:YES];
	}
    
    
    // Create transform to convert from vide frame coordinate space to view coordinate space
    CGAffineTransform t = [self affineTransformForVideoFrame:rect orientation:videoOrientation];

    
    const cv::Rect face = faces[0];
        
    CGRect faceRect;
    faceRect.origin.x = face.x;
    faceRect.origin.y = face.y;
    faceRect.size.width = face.width;
    faceRect.size.height = face.height;
    
    faceRect = CGRectApplyAffineTransform(faceRect, t);
    
    CALayer *faceFeatureLayer = nil;
    
    
    while (!faceFeatureLayer && (currentSublayer < sublayersCount)) {
        CALayer *currentLayer = [sublayers objectAtIndex:currentSublayer++];
        if ([[currentLayer name] isEqualToString:@"FaceLayer"]) {
            faceFeatureLayer = currentLayer;
            [currentLayer setHidden:NO];
        }
    }
    
    if (!faceFeatureLayer) {
        // Create a new feature marker layer
        faceFeatureLayer = [[CALayer alloc] init];
        faceFeatureLayer.name = @"FaceLayer";
        faceFeatureLayer.borderColor = [[UIColor redColor] CGColor];
        faceFeatureLayer.borderWidth = 10.0f;
        [self.view.layer addSublayer:faceFeatureLayer];
        [faceFeatureLayer release];
    }
    
    faceFeatureLayer.frame = faceRect;
    
    
    //narrow eye search to specific region of screen
    cv::Mat RoiImg = cv::Mat(mat, cv::Rect(face.x, face.y, (int)face.width*0.6, (int)face.height*0.75));
    
    std::vector<cv::Rect> eyes;
    
    CGRect eyeRect;
    
    //LEFT EYE
    _eyeCascade.detectMultiScale(RoiImg, eyes, 1.1, 2, kHaarOptions, cv::Size(20, 15));
    if(eyes.size() < 1) {
        start = nil;//reset time
        [CATransaction commit];
        return;
    }
    cv::Rect eye = eyes[0];
    
    eyeRect.origin.x = eye.x+face.x;
    eyeRect.origin.y = eye.y+face.y;
    eyeRect.size.width = eye.width;
    eyeRect.size.height = eye.height;
    
    
    
    eyeRect = CGRectApplyAffineTransform(eyeRect, t);
    
    CALayer *leftEyeFeatureLayer = nil;
    
    while (!leftEyeFeatureLayer && (currentSublayer < sublayersCount)) {
        CALayer *currentLayer = [sublayers objectAtIndex:currentSublayer++];
        if ([[currentLayer name] isEqualToString:@"LeftEyeLayer"]) {
            leftEyeFeatureLayer = currentLayer;
            [currentLayer setHidden:NO];
        }
    }
    
    if (!leftEyeFeatureLayer) {
        // Create a new feature marker layer
        leftEyeFeatureLayer = [[CALayer alloc] init];
        leftEyeFeatureLayer.name = @"LeftEyeLayer";
        leftEyeFeatureLayer.borderColor = [[UIColor purpleColor] CGColor];
        leftEyeFeatureLayer.borderWidth = 10.0f;
        [self.view.layer addSublayer:leftEyeFeatureLayer];
        [leftEyeFeatureLayer release];
    }
    
    leftEyeFeatureLayer.frame = eyeRect;
    
    
    
    
    
    
    int left_eye_end = eye.x+eye.width+face.x;
    int remaining_width = face.width + face.x - left_eye_end;
    
    
    //RIGHT EYE
    RoiImg = cv::Mat(mat, cv::Rect(
                                   left_eye_end, 
                                   face.y, 
                                   remaining_width,
                                   (int)face.height*0.75
                                   ));
    _eyeCascade.detectMultiScale(RoiImg, eyes, 1.1, 2, kHaarOptions, cv::Size(20, 15));
    
    if(eyes.size() < 1) {
        start = nil;//reset time
        [CATransaction commit];
        return;
    }
    //finally got everything for picture!
    
    eye = eyes[0];
    
    eyeRect.origin.x = eye.x+left_eye_end;
    eyeRect.origin.y = eye.y+face.y;
    eyeRect.size.width = eye.width;
    eyeRect.size.height = eye.height;
    
    eyeRect = CGRectApplyAffineTransform(eyeRect, t);
    
    CALayer *rightEyeFeatureLayer = nil;
    
    while (!rightEyeFeatureLayer && (currentSublayer < sublayersCount)) {
        CALayer *currentLayer = [sublayers objectAtIndex:currentSublayer++];
        if ([[currentLayer name] isEqualToString:@"RightEyeLayer"]) {
            rightEyeFeatureLayer = currentLayer;
            [currentLayer setHidden:NO];
        }
    }
    
    if (!rightEyeFeatureLayer) {
        // Create a new feature marker layer
        rightEyeFeatureLayer = [[CALayer alloc] init];
        rightEyeFeatureLayer.name = @"RightEyeLayer";
        rightEyeFeatureLayer.borderColor = [[UIColor orangeColor] CGColor];
        rightEyeFeatureLayer.borderWidth = 10.0f;
        [self.view.layer addSublayer:rightEyeFeatureLayer];
        [rightEyeFeatureLayer release];
    }
    
    rightEyeFeatureLayer.frame = eyeRect;
    [CATransaction commit];
    [self gotoConfirm];
    
}

@end
