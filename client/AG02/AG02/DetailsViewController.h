//
//  DetailsViewController.h
//  AG02
//
//  Created by デービット スクリプス on 8/18/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface DetailsViewController : UIViewController
{
    IBOutlet UIImageView *detailImageView;
}

- (void) initStuff:(NSString*)part;
- (IBAction)returnButton:(id)sender;
- (IBAction)saveButton:(id)sender;

@end
