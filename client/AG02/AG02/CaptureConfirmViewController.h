//
//  CaptureConfirmViewController.h
//  AG02
//
//  Created by デービット スクリプス on 8/3/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "ProgressViewController.h"

@interface CaptureConfirmViewController : UIViewController <UIAlertViewDelegate>
{
    UIProgressHUD *progressHUD;
    int last_camera;
    UIImage *faceImage;
    IBOutlet UIButton *againButton;
    IBOutlet UIButton *submitButton;
}

- (void)initStuff:(UIImage *)img camera:(int)camera;

- (IBAction)againButton:(id)sender;
- (IBAction)submitButton:(id)sender;


@end
