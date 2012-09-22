//
//  DetailsViewController.h
//  AG02
//
//  Created by デービット スクリプス on 8/18/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "GADBannerView.h"

@interface DetailsViewController : UIViewController
{
    IBOutlet UIImageView *detailImageView;
    GADBannerView *bannerView_;
    IBOutlet UITextView *partMessage;
    
    IBOutlet UIButton *returnButton;
}

- (void) initStuff:(NSString*)part;
- (IBAction)returnButton:(id)sender;
//- (IBAction)saveButton:(id)sender;

@end
