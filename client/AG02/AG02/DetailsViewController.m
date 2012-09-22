//
//  DetailsViewController.m
//  AG02
//
//  Created by デービット スクリプス on 8/18/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "DetailsViewController.h"
#import "ResultsViewController.h"

@interface DetailsViewController ()

@end

@implementation DetailsViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    // Do any additional setup after loading the view from its nib.
    
    [returnButton setTitle:NSLocalizedString(@"Back", @"") forState:UIControlStateNormal];
    [returnButton setTitle:NSLocalizedString(@"Back", @"") forState:UIControlStateHighlighted];
    [returnButton setTitle:NSLocalizedString(@"Back", @"") forState:UIControlStateDisabled];
    [returnButton setTitle:NSLocalizedString(@"Back", @"") forState:UIControlStateSelected];
    
    // Create a view of the standard size at the bottom of the screen.
    // Available AdSize constants are explained in GADAdSize.h.
    //bannerView_ = [[GADBannerView alloc] initWithAdSize:kGADAdSizeBanner];
    // Initialize the banner at the bottom of the screen.
    //CGPoint origin = CGPointMake(0.0, self.view.frame.size.height + 20 - CGSizeFromGADAdSize(kGADAdSizeBanner).height);
    CGPoint origin = CGPointMake(0.0, 0.0);
    
    // Use predefined GADAdSize constants to define the GADBannerView.
    bannerView_ = [[GADBannerView alloc] initWithAdSize:kGADAdSizeBanner origin:origin];
    
    // Specify the ad's "unit identifier." This is your AdMob Publisher ID.
    bannerView_.adUnitID = @"a1504f4c90f2afe";
    
    // Let the runtime know which UIViewController to restore after taking
    // the user wherever the ad goes and add it to the view hierarchy.
    bannerView_.rootViewController = self;
    [self.view addSubview:bannerView_];
    
    // Initiate a generic request to load it with an ad.
    [bannerView_ loadRequest:[GADRequest request]];
    [self.view addSubview:bannerView_];

    
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}
- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

- (void) initStuff:(NSString*)part {
    //NSString *part = @"left_eye";
    //NSString *part = @"forehead";
    NSString *urlStr = [NSString stringWithFormat:@"http://ec2-176-34-8-245.ap-northeast-1.compute.amazonaws.com/uploads/%@_result%@.jpg", [[NSUserDefaults standardUserDefaults] stringForKey:@"uuid"], part];
    detailImageView.image = [UIImage imageWithData:[NSData dataWithContentsOfURL:[NSURL URLWithString:urlStr]]];
    NSString *messageKey = [NSString stringWithFormat:@"message_%@", part];
    partMessage.text = [[NSUserDefaults standardUserDefaults] stringForKey:messageKey];
    NSLog(part);
    NSLog(messageKey);
    NSLog([[NSUserDefaults standardUserDefaults] stringForKey:messageKey]);
    NSLog(@"ok");
    /*NSString *uuid = [[NSUserDefaults standardUserDefaults] stringForKey:@"uuid"];
    [[NSUserDefaults standardUserDefaults] setObject:[responseDict valueForKey:@"message_forehead"] forKey:@"message_forehead"];
    [[NSUserDefaults standardUserDefaults] setObject:[responseDict valueForKey:@"message_left_eye"] forKey:@"message_left_eye"];
    [[NSUserDefaults standardUserDefaults] setObject:[responseDict valueForKey:@"message_right_eye"] forKey:@"message_right_eye"];
    [[NSUserDefaults standardUserDefaults] setObject:[responseDict valueForKey:@"message_nose_mouth"] forKey:@"message_nose_mouth"];*/
}


- (IBAction)returnButton:(id)sender
{
    //NSLog(@"return button");
    ResultsViewController *cV = [[[ResultsViewController alloc] initWithNibName:@"ResultsViewController" bundle:nil] autorelease];
    cV.modalTransitionStyle = UIModalTransitionStyleCrossDissolve;
    [self presentModalViewController:cV animated:YES];
    [self viewDidUnload];
}



@end
