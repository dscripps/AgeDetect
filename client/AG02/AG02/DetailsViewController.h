//
//  DetailsViewController.h
//  AG02
//
//  Created by デービット スクリプス on 8/18/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "GADBannerView.h"
#import "iAd/iAd.h"

@interface DetailsViewController : UIViewController <ADBannerViewDelegate>
{
    IBOutlet UIImageView *detailImageView;
    GADBannerView *bannerView_;
    IBOutlet ADBannerView *iAdView;
    
    IBOutlet UITextView *partMessage;
    
    IBOutlet UIButton *returnButton;
    
}

- (void) initStuff:(NSString*)part;
- (IBAction)returnButton:(id)sender;
//- (IBAction)saveButton:(id)sender;

@end
