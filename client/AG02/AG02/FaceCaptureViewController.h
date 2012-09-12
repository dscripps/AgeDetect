//
//  FaceCaptureViewController.h
//  AG02
//
//  Created by デービット スクリプス on 8/2/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "VCViewController.h"
#import "MBProgressHUD.h"
#import "GADBannerView.h"

//@interface FaceCaptureViewController : UIViewController
@interface FaceCaptureViewController : VCViewController
{
    cv::CascadeClassifier _faceCascade;
    cv::CascadeClassifier _eyeCascade;
    
    UIImage *currentImage;
    UIImage *faceImage;
    
    NSDate *start;
    
	MBRoundProgressView* progress;
    
    GADBannerView *bannerView_;
    
}

- (IBAction)toggleFps:(id)sender;
- (IBAction)toggleTorch:(id)sender;
- (IBAction)toggleCamera:(id)sender;

@end


