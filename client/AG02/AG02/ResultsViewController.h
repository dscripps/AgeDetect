//
//  ResultsViewController.h
//  AG02
//
//  Created by デービット スクリプス on 8/2/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "ProgressViewController.h"

@interface ResultsViewController : UIViewController
{
    UIProgressHUD *progressHUD;
    IBOutlet UILabel *ageLabel;
    NSString *currentPart;
}


- (void)initStuff;

- (IBAction)okButton:(id)sender;
- (IBAction)aboutButton:(id)sender;
- (IBAction)foreheadButton:(id)sender;
- (IBAction)leftEyeButton:(id)sender;
- (IBAction)rightEyeButton:(id)sender;
- (IBAction)mouthButton:(id)sender;

@end
