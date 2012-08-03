//
//  ViewController.m
//  AG02
//
//  Created by デービット スクリプス on 8/1/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "ViewController.h"
#import "DirectionsViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    if ([[UIDevice currentDevice] userInterfaceIdiom] == UIUserInterfaceIdiomPhone) {
        return (interfaceOrientation != UIInterfaceOrientationPortraitUpsideDown);
    } else {
        return YES;
    }
}

// MARK: IBActions

// start button
- (IBAction)start:(id)sender
{
    DirectionsViewController *DirectionsView = [[DirectionsViewController alloc] initWithNibName:@"DirectionsViewController" bundle:nil];
    DirectionsView.modalTransitionStyle = UIModalTransitionStyleCrossDissolve;
    [self presentModalViewController:DirectionsView animated:YES];
    //NSLog(@"START PRESSED!");
}


@end
