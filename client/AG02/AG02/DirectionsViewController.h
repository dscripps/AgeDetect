//
//  DirectionsViewController.h
//  AG02
//
//  Created by デービット スクリプス on 8/1/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "ProgressViewController.h"
#import "MBProgressHUD.h"
#import "GADBannerView.h"
#import "iAd/iAd.h"


@interface DirectionsViewController : UIViewController <ADBannerViewDelegate> {
    //UIProgressHUD *progressHUD;
    
    GADBannerView *bannerView_;
    IBOutlet ADBannerView *iAdView;
    
    IBOutlet UITextView *directions;
    IBOutlet UIButton *startButton;
}
    
- (IBAction)okButton:(id)sender;

@end
