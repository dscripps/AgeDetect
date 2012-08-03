//
//  DirectionsViewController.h
//  AG02
//
//  Created by デービット スクリプス on 8/1/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "ProgressViewController.h"



@interface DirectionsViewController : UIViewController {
    UIProgressHUD *progressHUD;
}
    
- (IBAction)okButton:(id)sender;

@end
