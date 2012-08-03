//
//  VCViewController.h
//  AG02
//
//  Created by デービット スクリプス on 8/2/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <AVFoundation/AVFoundation.h>

@interface VCViewController : UIViewController <AVCaptureVideoDataOutputSampleBufferDelegate>
{
    AVCaptureSession *_captureSession;
    AVCaptureDevice *_captureDevice;
    AVCaptureVideoDataOutput *_videoOutput;
    AVCaptureVideoPreviewLayer *_videoPreviewLayer;
    
    int _camera;
    NSString *_qualityPreset;
    BOOL _captureGrayscale;
    
    // Fps calculation
    CMTimeValue _lastFrameTimestamp;
    float *_frameTimes;
    int _frameTimesIndex;
    int _framesToAverage;
    
    float _captureQueueFps;
    float _fps;
    
    // Debug UI
    UILabel *_fpsLabel;
    
    UIImage *screenAsImage;

}
// Current frames per second
@property (nonatomic, readonly) float fps;

@property (nonatomic, assign) BOOL showDebugInfo;
@property (nonatomic, assign) BOOL torchOn;

// AVFoundation components
@property (nonatomic, readonly) AVCaptureSession *captureSession;
@property (nonatomic, readonly) AVCaptureDevice *captureDevice;
@property (nonatomic, readonly) AVCaptureVideoDataOutput *videoOutput;
@property (nonatomic, readonly) AVCaptureVideoPreviewLayer *videoPreviewLayer;


// -1: default, 0: back camera, 1: front camera
@property (nonatomic, assign) int camera;

// These should only be modified in the initializer
@property (nonatomic, assign) NSString * const qualityPreset;
@property (nonatomic, assign) BOOL captureGrayscale;

- (CGAffineTransform)affineTransformForVideoFrame:(CGRect)videoFrame orientation:(AVCaptureVideoOrientation)videoOrientation;

@end
